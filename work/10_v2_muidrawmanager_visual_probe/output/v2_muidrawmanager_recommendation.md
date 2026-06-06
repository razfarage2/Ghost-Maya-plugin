# V2.0A MUIDrawManager Recommendation

## Recommended Backend Path
**MPxDrawOverride + MUIDrawManager**

## Rationale
This architecture allows us to cleanly bypass all of the fatal memory-access bugs inherent in the Python 2.0 Viewport SubScene bindings. `MUIDrawManager.mesh()` natively draws geometry using robust Python classes like `MPointArray`, `MVectorArray`, and `MColorArray`. 
- **It does not crash in headless mode:** Meaning we can thoroughly test it in CI/CD environments.
- **It requires no external shaders:** The `MColorArray` applies RGBA values directly, guaranteeing our blue/red transparency tinting.
- **It is 100% DAG duplication-free:** It cleanly hooks into the hardware draw loop, never cluttering the Outliner.

## Should Stage 10B Proceed?
Yes, **after Raz confirms visual success**. 
If the interactive test proves the blue/red transparent ghosts appear correctly in the viewport, this architecture is officially greenlit for the Stage 10B production implementation.
