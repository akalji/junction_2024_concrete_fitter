import bpy
import random
import ifcopenshell

# Path to your IFC file
IFC_FILE_PATH = "/Users/akalji/Projects/Python/junction_2024_concrete_fitter/Dummy_Detailed_Fixed.ifc"  # Specify the correct path to your IFC file

# Loading the IFC file
ifc_file = ifcopenshell.open(IFC_FILE_PATH)

# Function to get all objects in the scene
def get_all_objects():
    """Returns a list of all 'MESH' type objects in the scene."""
    return [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

# Function to randomly select a specified number of objects
def select_random_objects(all_objects, num_objects=2):
    """Selects a random subset of objects from the list."""
    if len(all_objects) < num_objects:
        raise ValueError("Not enough objects in the scene for selection.")
    return random.sample(all_objects, num_objects)

# Function to apply materials to objects
def apply_materials_to_objects(all_objects, highlight_objects):
    """Applies materials to objects, highlighting specified objects in red."""
    for obj in all_objects:
        # Create a new material
        mat = bpy.data.materials.new(name=f"Material_{obj.name}")
        mat.use_nodes = False  # Disable nodes for simplicity

        # Set the material color depending on whether the object is highlighted
        if obj in highlight_objects:
            mat.diffuse_color = (1, 0, 0, 1)  # Bright red for highlighted objects
        else:
            mat.diffuse_color = (1, 1, 1, 0.3)  # Semi-transparent white for others
            mat.blend_method = 'BLEND'  # Transparent blend mode

        # Apply the material to the object
        if len(obj.data.materials):
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

# Class for selecting IFC element on click
class OBJECT_OT_select_ifc_element(bpy.types.Operator):
    """Operator for selecting an IFC element"""
    bl_idname = "object.select_ifc_element"
    bl_label = "Select IFC Element"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            obj = context.view_layer.objects.active
            if obj and obj.type == 'MESH':
                # Assume that the object's name corresponds to the element ID in the IFC file
                ifc_element_id = obj.name
                try:
                    # Retrieve the element from the IFC file by ID
                    ifc_element = ifc_file.by_id(int(ifc_element_id))

                    # Get the element's properties
                    properties = ifc_element.get_info()  # Read the element's information

                    # Print the ID and properties of the element to the console
                    print(f"ID: {ifc_element_id}")
                    print(f"Properties: {properties}")

                    # Return the ID and properties of the element to the WindowManager
                    context.window_manager.ifc_element_id = ifc_element_id
                    context.window_manager.ifc_properties = str(properties)

                    return {'FINISHED'}
                except Exception as e:
                    # Print an error message if not found
                    print(f"Element with ID {ifc_element_id} not found in the IFC file. Error: {e}")
                    return {'CANCELLED'}

        return {'RUNNING_MODAL'}

# Register the operator and properties
def register():
    bpy.utils.register_class(OBJECT_OT_select_ifc_element)
    bpy.types.WindowManager.ifc_element_id = bpy.props.StringProperty(name="IFC Element ID")
    bpy.types.WindowManager.ifc_properties = bpy.props.StringProperty(name="IFC Properties")

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_select_ifc_element)
    del bpy.types.WindowManager.ifc_element_id
    del bpy.types.WindowManager.ifc_properties

# Main function to perform all operations
def main():
    """Main function to highlight objects, apply materials, and initialize IFC element selection."""
    # Get all objects and select two random ones
    all_objects = get_all_objects()
    highlight_objects = select_random_objects(all_objects, 2)
    apply_materials_to_objects(all_objects, highlight_objects)

    # Start the operator to select IFC elements on click
    bpy.ops.object.select_ifc_element('INVOKE_DEFAULT')
    print("Script executed: two objects highlighted in red, others are semi-transparent.")

if __name__ == "__main__":
    register()
    main()
