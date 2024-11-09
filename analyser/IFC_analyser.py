import ifcopenshell
from shapely.geometry import box, Polygon

# Порог расстояния в метрах (1.5 см)
PROXIMITY_THRESHOLD = 0.015

def get_elements_by_type(ifc_file, types):
    """Получает все элементы указанных IFC-типов."""
    elements = []
    for element_type in types:
        elements += ifc_file.by_type(element_type)
    return elements

def extract_bounding_box(element):
    """Извлекает границы элемента, проверяя различные возможные представления."""
    try:
        # Перебираем представления элемента
        shape_rep = element.Representation.Representations[0]
        for item in shape_rep.Items:
            if item.is_a("IFCEXTRUDEDAREASOLID"):
                # Извлекаем минимальные и максимальные координаты из профиля
                profile = item.SweptArea
                if profile.is_a("IFCRECTANGLEPROFILEDEF"):
                    x_min = -profile.XDim / 2
                    x_max = profile.XDim / 2
                    y_min = -profile.YDim / 2
                    y_max = profile.YDim / 2
                    bbox = box(x_min, y_min, x_max, y_max)
                    return bbox
            elif item.is_a("IFCPOLYLINE"):
                vertices = [(point[0], point[1]) for point in item.Points]
                if vertices:
                    x_min = min(v[0] for v in vertices)
                    y_min = min(v[1] for v in vertices)
                    x_max = max(v[0] for v in vertices)
                    y_max = max(v[1] for v in vertices)
                    bbox = box(x_min, y_min, x_max, y_max)
                    return bbox
            elif item.is_a("IFCMAPPEDITEM"):
                # Раскрываем геометрию, связанную с `IFCMAPPEDITEM`
                mapping_source = item.MappingSource
                mapped_rep = mapping_source.MappedRepresentation
                for mapped_item in mapped_rep.Items:
                    if mapped_item.is_a("IFCEXTRUDEDAREASOLID"):
                        profile = mapped_item.SweptArea
                        if profile.is_a("IFCRECTANGLEPROFILEDEF"):
                            x_min = -profile.XDim / 2
                            x_max = profile.XDim / 2
                            y_min = -profile.YDim / 2
                            y_max = profile.YDim / 2
                            bbox = box(x_min, y_min, x_max, y_max)
                            return bbox
                    elif mapped_item.is_a("IFCPOLYLINE"):
                        vertices = [(point[0], point[1]) for point in mapped_item.Points]
                        if vertices:
                            x_min = min(v[0] for v in vertices)
                            y_min = min(v[1] for v in vertices)
                            x_max = max(v[0] for v in vertices)
                            y_max = max(v[1] for v in vertices)
                            bbox = box(x_min, y_min, x_max, y_max)
                            return bbox
    except AttributeError:
        return None
    return None

def check_collision_or_proximity(bbox1, bbox2, threshold):
    """Проверяет пересечение или близость двух боксов."""
    if bbox1.intersects(bbox2):
        return True
    return bbox1.distance(bbox2) <= threshold

def find_collisions(ifc_file, element_types, threshold):
    """Ищет коллизии или близко расположенные пары элементов среди указанных типов."""
    elements = get_elements_by_type(ifc_file, element_types)
    collision_pairs = []
    for i, element1 in enumerate(elements):
        bbox1 = extract_bounding_box(element1)
        if bbox1:
            for j, element2 in enumerate(elements[i+1:], start=i+1):
                bbox2 = extract_bounding_box(element2)
                if bbox2:
                    if check_collision_or_proximity(bbox1, bbox2, threshold):
                        collision_pairs.append((element1.id(), element2.id()))
#    unique_elements = set()
    # Проходим по каждой паре и добавляем оба элемента в множество
#    for pair in collision_pairs:
#        unique_elements.update(pair)
    # Преобразуем множество в список (если это нужно) и выводим результат
#    unique_elements_list = list(unique_elements)
    return collision_pairs

# Загрузка IFC файла
file_path = 'C:/Users/Костя/Downloads/Dummy_Detailed_Fixed.ifc'
ifc_file = ifcopenshell.open(file_path)

# Типы элементов для поиска
ELEMENT_TYPES = ["IFCSLAB", "IFCWALL", "IFCBEAM", "IFCCOLUMN"]

# Поиск коллизий
collision_pairs = find_collisions(ifc_file, ELEMENT_TYPES, PROXIMITY_THRESHOLD)