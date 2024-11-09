import bpy
import random
import ifcopenshell

# Путь к вашему IFC файлу
IFC_FILE_PATH = "/Users/akalji/Projects/Python/junction_2024_concrete_fitter/Dummy_Detailed_Fixed.ifc"  # Укажите правильный путь к вашему IFC файлу

# Загрузка IFC файла
ifc_file = ifcopenshell.open(IFC_FILE_PATH)

# Функция для получения всех объектов сцены
def get_all_objects():
    """Возвращает список всех объектов типа 'MESH' в сцене."""
    return [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

# Функция для случайного выбора заданного количества объектов
def select_random_objects(all_objects, num_objects=2):
    """Выбирает случайное подмножество объектов из списка."""
    if len(all_objects) < num_objects:
        raise ValueError("Недостаточно объектов в сцене для выборки.")
    return random.sample(all_objects, num_objects)

# Функция для применения материалов к объектам
def apply_materials_to_objects(all_objects, highlight_objects):
    """Применяет материалы к объектам, выделяя указанные объекты красным цветом."""
    for obj in all_objects:
        # Создание нового материала
        mat = bpy.data.materials.new(name=f"Material_{obj.name}")
        mat.use_nodes = False  # Отключаем узлы для простоты

        # Устанавливаем цвет материала в зависимости от того, выделен объект или нет
        if obj in highlight_objects:
            mat.diffuse_color = (1, 0, 0, 1)  # Ярко-красный для выделенных объектов
        else:
            mat.diffuse_color = (1, 1, 1, 0.3)  # Полупрозрачный белый для остальных
            mat.blend_method = 'BLEND'  # Прозрачный метод смешивания

        # Применяем материал к объекту
        if len(obj.data.materials):
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

# Класс для выделения IFC элемента при клике
class OBJECT_OT_select_ifc_element(bpy.types.Operator):
    """Оператор для выделения IFC элемента"""
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

# Регистрация оператора и свойств
def register():
    bpy.utils.register_class(OBJECT_OT_select_ifc_element)
    bpy.types.WindowManager.ifc_element_id = bpy.props.StringProperty(name="IFC Element ID")
    bpy.types.WindowManager.ifc_properties = bpy.props.StringProperty(name="IFC Properties")

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_select_ifc_element)
    del bpy.types.WindowManager.ifc_element_id
    del bpy.types.WindowManager.ifc_properties

# Основная функция для выполнения всех операций
def main():
    """Основная функция для выделения объектов, применения материалов и инициализации IFC обработки."""
    # Получаем все объекты и выделяем два случайных
    all_objects = get_all_objects()
    highlight_objects = select_random_objects(all_objects, 2)
    apply_materials_to_objects(all_objects, highlight_objects)

    # Запускаем оператор для выбора IFC элементов при клике
    bpy.ops.object.select_ifc_element('INVOKE_DEFAULT')
    print("Скрипт выполнен: два объекта выделены красным, остальные полупрозрачны.")

if __name__ == "__main__":
    register()
    main()
