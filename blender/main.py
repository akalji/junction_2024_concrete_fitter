import bpy
import random

# Function to get all objects in the scene
def get_all_objects():
    return [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

# Get a list of all objects
all_objects = get_all_objects()

# Check if there are enough objects for selection
if len(all_objects) < 2:
    raise ValueError("Not enough objects in the scene for selection.")

# Select two random objects
highlight_objects = random.sample(all_objects, 2)

# Apply materials to objects
for obj in all_objects:
    # Create a new material
    mat = bpy.data.materials.new(name=f"Material_{obj.name}")
    mat.use_nodes = False  # Disable nodes for simplicity

    if obj in highlight_objects:
        # Set a bright red color for selected objects
        mat.diffuse_color = (1, 0, 0, 1)  # RGBA
    else:
        # Set a semi-transparent color for all other objects
        mat.diffuse_color = (1, 1, 1, 0.3)  # RGBA (semi-transparent white)
        mat.blend_method = 'BLEND'  # Transparent blend method

    # Apply the material to the object
    if len(obj.data.materials):
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

print("Script executed: two objects are highlighted in red, others are semi-transparent.")
