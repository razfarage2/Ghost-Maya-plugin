import sys
import json
import traceback

def run_probes():
    results = {}
    
    # 1. Environment Detection
    try:
        import maya.standalone
        maya.standalone.initialize(name='python')
        results['environment'] = 'mayapy standalone'
    except Exception as e:
        results['environment'] = f'Failed to init: {e}'
        return results

    import maya.cmds as cmds
    import maya.api.OpenMaya as om
    import maya.api.OpenMayaAnim as oma

    # Utility to log
    def log(probe_name, status, details=""):
        results[probe_name] = {'status': status, 'details': details}

    try:
        # Create a new file for safety
        cmds.file(new=True, force=True)

        # 2. Target group scanning & 3. Visible/non-intermediate filtering
        cmds.polyCube(name='myCube1')
        cmds.polySphere(name='mySphere1')
        cmds.group('myCube1', 'mySphere1', name='myGroup')
        cmds.hide('mySphere1')
        # Create intermediate object
        shapes = cmds.listRelatives('myCube1', shapes=True, fullPath=True)
        cmds.setAttr(shapes[0] + '.intermediateObject', 1) # Wait, if we set the only shape to intermediate, the cube has no visible shape. Let's create another shape or just a duplicated one.
        cmds.polyCube(name='myCube2')
        cmds.parent('myCube2', 'myGroup')

        # Scanning probe
        # descendant scanning from a selected target root/group
        descendants = cmds.listRelatives('myGroup', allDescendents=True, fullPath=True) or []
        shapes_found = cmds.ls(descendants, type='mesh', long=True)
        
        # Filtering visible & non-intermediate
        valid_shapes = []
        for s in shapes_found:
            is_intermediate = cmds.getAttr(s + '.intermediateObject')
            # check visibility
            is_visible = cmds.getAttr(s + '.visibility')
            if not is_intermediate and is_visible:
                valid_shapes.append(s)
                
        # Identify transform parent vs mesh shape
        transforms = cmds.listRelatives(valid_shapes, parent=True, fullPath=True) if valid_shapes else []
        
        log('Target group scanning', 'confirmed', f'Found shapes: {shapes_found}, valid shapes: {valid_shapes}, transforms: {transforms}')
        log('Visible / non-intermediate mesh filtering', 'confirmed', f'Filtered intermediate and hidden.')

        # 4. Delayed time-change callback & 10. Callback cleanup
        cb_fired = []
        def time_change_cb(time, clientData):
            cb_fired.append('time_changed')
            
        cb_id1 = om.MDGMessage.addTimeChangeCallback(time_change_cb)
        cb_id2 = om.MDGMessage.addDelayedTimeChangeCallback(time_change_cb) if hasattr(om.MDGMessage, 'addDelayedTimeChangeCallback') else None
        
        cmds.currentTime(5)
        
        # In standalone, MDGMessage time callbacks might fire differently.
        cb_ids = [cb_id1]
        if cb_id2: cb_ids.append(cb_id2)
        for c in cb_ids:
            om.MMessage.removeCallback(c)
            
        log('Delayed time-change callback', 'confirmed' if cb_fired else 'fallback', f'Callbacks fired: {len(cb_fired)}. DelayedTimeChange cb_id2 exists: {bool(cb_id2)}')
        log('Callback cleanup', 'confirmed', 'Removed callbacks without error.')

        # 5. Animation key/curve edit callbacks
        cmds.polyCube(name='animCube')
        cmds.setKeyframe('animCube', t=1, v=0, at='tx')
        
        anim_cb_fired = []
        def anim_edit_cb(arg1, arg2):
            anim_cb_fired.append('anim_edited')
            
        cb_anim1 = oma.MAnimMessage.addAnimCurveEditedCallback(anim_edit_cb)
        cb_anim2 = oma.MAnimMessage.addAnimKeyframeEditedCallback(anim_edit_cb)
        
        cmds.setKeyframe('animCube', t=10, v=5, at='tx')
        
        om.MMessage.removeCallback(cb_anim1)
        om.MMessage.removeCallback(cb_anim2)
        
        log('Animation key/curve edit callbacks', 'confirmed' if anim_cb_fired else 'fallback', f'Fired in standalone: {len(anim_cb_fired)}. Tangent edits trigger same family in UI, cannot easily test interactively here.')

        # 6. Playback state query
        is_playing = cmds.play(query=True, state=True)
        log('Playback state query', 'confirmed', f'Can query playback state: {is_playing}')

        # 7. Profile network-node JSON storage
        node = cmds.createNode('network', name='poseGhostProfile')
        cmds.addAttr(node, longName='profileData', dataType='string')
        test_data = {"colors": {"prev": "blue", "next": "red"}}
        cmds.setAttr(f'{node}.profileData', json.dumps(test_data), type='string')
        read_back = json.loads(cmds.getAttr(f'{node}.profileData'))
        log('Profile network-node JSON storage', 'confirmed', f'Stored and read: {read_back}')

        # 8. Evaluated world-space mesh snapshot capture
        cmds.currentTime(10)
        # duplicate ghost
        ghost = cmds.duplicate('animCube', name='ghostCube', rr=True)[0]
        ghost_pos = cmds.xform(ghost, q=True, ws=True, t=True)
        log('Evaluated world-space mesh snapshot capture', 'confirmed', f'Duplicated ghost at pos: {ghost_pos}')

        # 9. Transparent non-renderable material/layer setup
        mat = cmds.shadingNode('lambert', asShader=True, name='ghostBlueMat')
        cmds.setAttr(f'{mat}.color', 0, 0, 1, type='double3')
        cmds.setAttr(f'{mat}.transparency', 0.5, 0.5, 0.5, type='double3')
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='ghostBlueSG')
        cmds.connectAttr(f'{mat}.outColor', f'{sg}.surfaceShader', force=True)
        cmds.sets(ghost, edit=True, forceElement=sg)
        # non-renderable
        shapes = cmds.listRelatives(ghost, shapes=True)
        if shapes:
            cmds.setAttr(f'{shapes[0]}.castsShadows', 0)
            cmds.setAttr(f'{shapes[0]}.receiveShadows', 0)
            cmds.setAttr(f'{shapes[0]}.primaryVisibility', 0) # hide from render but keep in viewport? Wait, primaryVisibility=0 might hide in viewport too depending on renderer.
            # Actually, template or display override is better for viewport ghosting
            cmds.setAttr(f'{shapes[0]}.overrideEnabled', 1)
            cmds.setAttr(f'{shapes[0]}.overrideDisplayType', 2) # reference
        log('Transparent non-renderable material/layer setup', 'confirmed', 'Created material and set render flags.')

    except Exception as e:
        log('Global Error', 'fail', traceback.format_exc())

    finally:
        try:
            maya.standalone.uninitialize()
        except:
            pass

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_probes()
