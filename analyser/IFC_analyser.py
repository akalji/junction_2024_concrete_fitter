import ifcopenshell
from shapely.geometry import box

# Порог расстояния в метрах (1.5 см)
PROXIMITY_THRESHOLD = 0.015

class IFCAnalyser:
    def __init__(self, ifc_file_path, element_types, threshold=PROXIMITY_THRESHOLD):
        self.ifc_file = ifcopenshell.open(ifc_file_path)
        self.element_types = element_types
        self.threshold = threshold

    def get_elements_by_type(self):
        """Получает все элементы указанных IFC-типов."""
        elements = []
        for element_type in self.element_types:
            elements += self.ifc_file.by_type(element_type)
        return elements

    def extract_bounding_box(self, element):
        """Извлекает границы элемента, проверяя различные возможные представления."""
        try:
            shape_rep = element.Representation.Representations[0]
            for item in shape_rep.Items:
                if item.is_a("IFCEXTRUDEDAREASOLID"):
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
        except AttributeError:
            return None
        return None

    def check_collision_or_proximity(self, bbox1, bbox2):
        """Проверяет пересечение или близость двух боксов."""
        if bbox1.intersects(bbox2):
            return True
        return bbox1.distance(bbox2) <= self.threshold

    def find_collisions(self):
        """Ищет коллизии или близко расположенные пары элементов среди указанных типов."""
        elements = self.get_elements_by_type()
        collision_pairs = []
        for i, element1 in enumerate(elements):
            bbox1 = self.extract_bounding_box(element1)
            if bbox1:
                for j, element2 in enumerate(elements[i+1:], start=i+1):
                    bbox2 = self.extract_bounding_box(element2)
                    if bbox2:
                        if self.check_collision_or_proximity(bbox1, bbox2):
                            collision_pairs.append((element1.id(), element2.id()))
        return collision_pairs
