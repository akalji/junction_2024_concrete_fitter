from IFC_analyser import IFCAnalyser

# Путь к IFC файлу
ifc_file_path = 'C:/Users/Костя/Downloads/Dummy_Detailed_Fixed.ifc'

# Типы элементов, которые будем искать
element_types = ["IFCSLAB", "IFCWALL", "IFCBEAM", "IFCCOLUMN"]

# Создаем экземпляр класса IFCAnalyser
collision_detector = IFCAnalyser(ifc_file_path, element_types)
print(collision_detector.collision_pairs)
print(collision_detector.collided_elements)
# Находим коллизии
collision_pairs = collision_detector.find_collisions()
