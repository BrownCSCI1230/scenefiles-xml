# CSCI1230 Scenefiles

This repo contains scenefiles for CSCI1230. The scenefiles are grouped in the following directories.

- `test_intersect`: Simple scenes with small number of primitives. It contains tests for phong effect, divided and combined.

- `test_unit`: Scenes with a single primitive and directional light. It can be used for testing whether the normals for shapes are correct.

- `test_efficiency`: Scenes with a relative large number of primitives. It generally takes longer to render and can be used to evaluate program efficiency.

- `test_light`: Scenes that focus on different light sources. It contains tests for directional light, spotlight and point light.

- `test_feature`: Scenes for the `Project 6: Illuminate`. It contains tests for complex features: shadow, reflection and texture mapping.

- `test_fun`: Scenes with interesting themes, that can be used for fun.

- `test_legacy`: Scenes migrated from the legacy CSCI1230 scenefile folder.


It would take a significant amount of time to render any scene in the below test groups with a baseline implementation of ray-tracer.

- `test_take_forever`: Extremely large scenes that are almost impossible to be rendered by baseline ray tracer implementation. They can be used to test optimizations such as multithreading and acceleration data structure. `recursiveSphere1 ~ 6` are still included for completeness purpose only.

- `test_refract`: Scenes for testing refraction.

- `test_dof`: Scenes for testing depth of field.
 
- `test_mesh`: Scenes where meshes are loaded as primitives and can be used for testing mesh loading and ray-triangle intersection.

