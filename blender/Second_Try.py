import bpy
import ifcopenshell

# Путь к вашему IFC файлу
IFC_FILE_PATH = "C:/path/to/your/file.ifc"  # Заполните правильный путь к вашему IFC файлу

# Загрузка IFC файла
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
            # Получаем объект, на который кликнули
            obj = context.view_layer.objects.active
            if obj and obj.type == 'MESH':
                # Предполагаем, что имя объекта соответствует ID элемента в IFC файле
                ifc_element_id = obj.name
                try:
                    # Извлекаем элемент из IFC файла по ID
                    ifc_element = ifc_file.by_id(int(ifc_element_id))

                    # Получаем свойства элемента
                    properties = ifc_element.get_info()  # Считываем информацию об элементе

                    # Выводим ID и свойства элемента в консоль
                    print(f"ID: {ifc_element_id}")
                    print(f"Properties: {properties}")

                    # Возвращаем ID и свойства элемента в WindowManager
                    context.window_manager.ifc_element_id = ifc_element_id
                    context.window_manager.ifc_properties = str(properties)

                    return {'FINISHED'}
                except Exception as e:
                    # В случае ошибки выводим сообщение об ошибке
                    print(f"Элемент с ID {ifc_element_id} не найден в IFC файле. Ошибка: {e}")
                    return {'CANCELLED'}

        return {'RUNNING_MODAL'}

# Регистрация оператора
def register():
    bpy.utils.register_class(OBJECT_OT_select_ifc_element)
    bpy.types.WindowManager.ifc_element_id = bpy.props.StringProperty(name="IFC Element ID")
    bpy.types.WindowManager.ifc_properties = bpy.props.StringProperty(name="IFC Properties")

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_select_ifc_element)
    del bpy.types.WindowManager.ifc_element_id
    del bpy.types.WindowManager.ifc_properties

if __name__ == "__main__":  # Исправлено имя с 'name' на '__name__'
    register()
    # Вызовите оператор для запуска
    bpy.ops.object.select_ifc_element('INVOKE_DEFAULT')
