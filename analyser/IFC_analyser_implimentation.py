from IFC_analyser import IFCAnalyser

# Путь к IFC файлу
ifc_file_path = 'C:/Users/Костя/Downloads/Dummy_Detailed_Fixed.ifc'

# Типы элементов, которые будем искать
element_types = ["IFCSLAB", "IFCWALL", "IFCBEAM", "IFCCOLUMN"]

# Создаем экземпляр класса IFCAnalyser
collision_detector = IFCAnalyser(ifc_file_path, element_types)

# Находим коллизии
collision_pairs = collision_detector.find_collisions()

# Выводим пары коллизий
print("Найденные пары коллизий:")
for pair in collision_pairs:
    print(f"Коллизия между элементами с ID: {pair[0]} и {pair[1]}")
