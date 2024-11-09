import bpy
import random

# Функция для получения всех объектов сцены
def get_all_objects():
    return [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

# Получаем список всех объектов
all_objects = get_all_objects()

# Проверяем, есть ли достаточно объектов для выборки
if len(all_objects) < 2:
    raise ValueError("Недостаточно объектов в сцене для выделения.")

# Выбираем два случайных объекта
highlight_objects = random.sample(all_objects, 2)

# Применение материалов к объектам
for obj in all_objects:
    # Создание нового материала
    mat = bpy.data.materials.new(name=f"Material_{obj.name}")
    mat.use_nodes = False  # Отключаем узлы для простоты

    if obj in highlight_objects:
        # Устанавливаем ярко-красный цвет для выбранных объектов
        mat.diffuse_color = (1, 0, 0, 1)  # RGBA
    else:
        # Устанавливаем полупрозрачный цвет для всех остальных
        mat.diffuse_color = (1, 1, 1, 0.3)  # RGBA (прозрачный белый)
        mat.blend_method = 'BLEND'  # Прозрачный метод смешивания

    # Применяем материал к объекту
    if len(obj.data.materials):
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

print("Скрипт выполнен: два объекта выделены красным, остальные полупрозрачны.")