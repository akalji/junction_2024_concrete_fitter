from IFC_analyser import IFCAnalyser
from IFC_Material_Extractor import IFCMaterialExtractor
from product_recommendation import ProductMapper

class IFCProductRecommender:
    def __init__(self, ifc_file_path, element_types, json_file="analyser/product_mapping_schema.json"):
        self.analyser = IFCAnalyser(ifc_file_path, element_types)
        self.material_extractor = IFCMaterialExtractor(ifc_file_path)
        self.product_mapper = ProductMapper(json_file)

    def find_recommended_product(self, line_number):
        # Проверяем, есть ли коллизии с элементом по заданному номеру строки
        for element1_id, element2_id in self.analyser.collision_pairs:
            if line_number in (element1_id, element2_id):
                # Получаем материалы и типы обоих элементов
                element1_type = self.get_element_type_by_id(element1_id)
                element2_type = self.get_element_type_by_id(element2_id)
                element1_material = self.material_extractor.get_material_type(element1_id)
                element2_material = self.material_extractor.get_material_type(element2_id)

                # Определяем типы для передачи в ProductMapper
                instance1 = element1_type.lower()
                instance2 = element2_type.lower()

                # Ищем продукт согласно JSON схеме
                product = self.product_mapper.find_product(instance1, instance2, element1_material, element2_material)
                if product:
                    return product

        return "Подходящий продукт не найден"

    def get_element_type_by_id(self, element_id):
        """Возвращает тип элемента по его ID."""
        element = self.analyser.ifc_file.by_id(element_id)
        if element:
            return element.is_a().replace("IFC", "").lower()
        return "unknown"

ifc_path = "C:/Users/Костя/Downloads/Dummy_Detailed_Fixed.ifc"
line_number = 14559
element_types = ["IFCBEAM", "IFCCOLUMN", "IFCWALL", "IFCSLAB"]

recommender = IFCProductRecommender(ifc_path, element_types)
recommended_product = recommender.find_recommended_product(line_number)
print(f"Рекомендованный продукт: {recommended_product}")