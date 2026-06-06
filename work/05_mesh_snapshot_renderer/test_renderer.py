import sys
import json
import traceback

def run_tests():
    results = {}
    
    try:
        import maya.standalone
        maya.standalone.initialize(name='python')
    except Exception as e:
        print(json.dumps({"error": f"Failed to init Maya: {e}"}))
        return

    import maya.cmds as cmds
    
    # We must add the src directory to sys.path to import pose_ghost
    import os
    sys.path.append(os.path.abspath('src'))
    
    from pose_ghost.maya_adapters import (
        TargetScanner, MeshTargetAdapter, EvaluatedSnapshotCapture,
        MeshSnapshotRenderer, MaterialManager, DisplayLayerManager,
        ObjectBypassStore, ProxySourceResolver, SceneProfileStore
    )
    from pose_ghost.core import SamplePlan, OnionSample

    def log(test_name, status, details=""):
        results[test_name] = {'status': status, 'details': details}

    try:
        cmds.file(new=True, force=True)

        # 1-4. Target Scanner
        cmds.polyCube(name='visibleMesh')
        cmds.polySphere(name='hiddenMesh')
        cmds.hide('hiddenMesh')
        cmds.polyCone(name='intermediateMesh')
        shapes = cmds.listRelatives('intermediateMesh', shapes=True, fullPath=True)
        cmds.setAttr(f"{shapes[0]}.intermediateObject", 1)
        cmds.group('visibleMesh', 'hiddenMesh', 'intermediateMesh', name='testGroup')
        cmds.group(empty=True, name='PoseGhostGrp') # Fake pose ghost group
        
        targets = TargetScanner.scan_target_root('testGroup')
        
        log('Target scanner visibility/intermediate filtering', 
            'confirmed' if len(targets) == 1 and 'visibleMesh' in targets[0] else 'fail',
            f'Found: {targets}')

        # 5-6. Evaluated Snapshot Capture
        cmds.setKeyframe('visibleMesh', t=1, v=0, at='tx')
        cmds.setKeyframe('visibleMesh', t=10, v=10, at='tx')
        
        cmds.currentTime(1)
        ghost = EvaluatedSnapshotCapture.capture_snapshot('visibleMesh', 10.0, 'ghostTest')
        
        # Verify it snapped to frame 10 position (tx=10)
        ghost_tx = cmds.getAttr(f"{ghost}.tx")
        
        # Source at frame 1 should still be 0
        src_tx = cmds.getAttr('visibleMesh.tx')
        
        log('Evaluated Snapshot Position & Independence', 
            'confirmed' if abs(ghost_tx - 10.0) < 0.001 and abs(src_tx - 0.0) < 0.001 else 'fail',
            f'Ghost TX: {ghost_tx}, Src TX: {src_tx}')

        # 7-14. Mesh Snapshot Renderer
        cmds.file(new=True, force=True)
        cube = cmds.polyCube(name='animCube')[0]
        cmds.setKeyframe(cube, t=10, v=0, at='tx')
        cmds.setKeyframe(cube, t=20, v=10, at='tx')
        cmds.setKeyframe(cube, t=30, v=20, at='tx')
        
        orig_mat = cmds.listConnections(cmds.listHistory(cube, future=True), type='shadingEngine')
        orig_mat_count = len(set(orig_mat)) if orig_mat else 0
        orig_keys = cmds.keyframe(cube, query=True, timeChange=True)
        
        plan = SamplePlan()
        plan.previous_samples.append(OnionSample(frame=10.0, side='previous', index=1, opacity=0.5))
        plan.previous_samples.append(OnionSample(frame=15.0, side='previous', index=2, opacity=0.25))
        plan.next_samples.append(OnionSample(frame=30.0, side='next', index=1, opacity=0.5))
        
        MeshSnapshotRenderer.render(plan, [cube])
        
        # Verify groups and ghosts exist
        prev_grp_exists = cmds.objExists("PoseGhostPreviousGrp")
        next_grp_exists = cmds.objExists("PoseGhostNextGrp")
        
        # Verify materials
        mat1 = "PoseGhostPreviousMat_1"
        mat2 = "PoseGhostPreviousMat_2"
        mat3 = "PoseGhostNextMat_1"
        
        mats_exist = cmds.objExists(mat1) and cmds.objExists(mat2) and cmds.objExists(mat3)
        if mats_exist:
            col1 = cmds.getAttr(f"{mat1}.color")[0]
            col3 = cmds.getAttr(f"{mat3}.color")[0]
            trans1 = cmds.getAttr(f"{mat1}.transparency")[0]
            trans2 = cmds.getAttr(f"{mat2}.transparency")[0]
        else:
            col1 = col3 = trans1 = trans2 = None

        # Verify source unchanged
        post_mat = cmds.listConnections(cmds.listHistory(cube, future=True), type='shadingEngine')
        post_mat_count = len(set(post_mat)) if post_mat else 0
        post_keys = cmds.keyframe(cube, query=True, timeChange=True)
        
        MeshSnapshotRenderer.cleanup()
        cleaned = not cmds.objExists("PoseGhostGrp")
        
        log('Mesh Snapshot Renderer full test', 
            'confirmed' if prev_grp_exists and mats_exist and cleaned and orig_keys == post_keys and orig_mat_count == post_mat_count else 'fail',
            f'Mats exist: {mats_exist}. Colors matched logic: {col1==(0,0,1) and col3==(1,0,0)}. Falloff logic trans: {trans1[0]==0.5 and trans2[0]==0.75}')

        # 15. Object Bypass Store
        bypass = ObjectBypassStore()
        bypass.mark_bypassed('objA')
        filtered = bypass.filter_targets(['objA', 'objB'])
        log('Object bypass', 'confirmed' if filtered == ['objB'] else 'fail', str(filtered))
        
        # 16. Proxy Source Resolver
        cmds.group(empty=True, name='myProxy')
        res1 = ProxySourceResolver.resolve('myOrig', 'myProxy', 'proxy')
        res2 = ProxySourceResolver.resolve('myOrig', 'missingProxy', 'proxy')
        log('Proxy Source Resolver', 'confirmed' if res1 == 'myProxy' and res2 == 'myOrig' else 'fail', f'{res1}, {res2}')
        
        # 17. Scene Profile Store
        cmds.file(new=True, force=True)
        test_data = {"test": 123}
        SceneProfileStore.save_profile(test_data)
        loaded = SceneProfileStore.load_profile()
        log('Scene Profile Store', 'confirmed' if loaded == test_data else 'fail', str(loaded))

    except Exception as e:
        log('Global Error', 'fail', traceback.format_exc())

    finally:
        try:
            maya.standalone.uninitialize()
        except:
            pass

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_tests()
