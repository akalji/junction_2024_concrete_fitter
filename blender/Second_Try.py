import bpy
import ifcopenshell

# Path to your IFC file
IFC_FILE_PATH = "C:/path/to/your/file.ifc"  # Fill in the correct path to your IFC file

# Loading the IFC file
ifc_file = ifcopenshell.open(IFC_FILE_PATH)

class OBJECT_OT_select_ifc_element(bpy.types.Operator):
    bl_idname = "object.select_ifc_element"
    bl_label = "Select IFC Element"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Get the object that was clicked on
            obj = context.view_layer.objects.active
            if obj and obj.type == 'MESH':
                # Assume that the object's name matches the ID of an element in the IFC file
                ifc_element_id = obj.name
                try:
                    # Retrieve the element from the IFC file by ID
                    ifc_element = ifc_file.by_id(int(ifc_element_id))

                    # Get the element's properties
                    properties = ifc_element.get_info()  # Read information about the element

                    # Print the element ID and properties to the console
                    print(f"ID: {ifc_element_id}")
                    print(f"Properties: {properties}")

                    # Return the element ID and properties to the WindowManager
                    context.window_manager.ifc_element_id = ifc_element_id
                    context.window_manager.ifc_properties = str(properties)

                    return {'FINISHED'}
                except Exception as e:
                    # Print an error message if there is an issue
                    print(f"Element with ID {ifc_element_id} not found in the IFC file. Error: {e}")
                    return {'CANCELLED'}

        return {'RUNNING_MODAL'}

# Registering the operator
def register():
    bpy.utils.register_class(OBJECT_OT_select_ifc_element)
    bpy.types.WindowManager.ifc_element_id = bpy.props.StringProperty(name="IFC Element ID")
    bpy.types.WindowManager.ifc_properties = bpy.props.StringProperty(name="IFC Properties")

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_select_ifc_element)
    del bpy.types.WindowManager.ifc_element_id
    del bpy.types.WindowManager.ifc_properties

if __name__ == "__main__":  # Fixed the name from 'name' to '__name__'
    register()
    # Call the operator to start
    bpy.ops.object.select_ifc_element('INVOKE_DEFAULT')
