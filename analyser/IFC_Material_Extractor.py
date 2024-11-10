import ifcopenshell


class IFCMaterialExtractor:
    def __init__(self, ifc_file_path):
        # Load the IFC file
        self.ifc_file = ifcopenshell.open(ifc_file_path)

    def get_material_type(self, line_number):
        # Get the IFC element by line number
        element = self.ifc_file.by_id(line_number)

        if element:
            # Access the last attribute in the element for material info
            attributes = element.get_info()  # Get all attributes as a dictionary
            material_name = list(attributes.values())[-1]  # Access the last attribute

            # Convert material_name to lowercase for comparison, handle if it's None
            material_name = material_name.lower() if material_name else ""

            # Material classification logic
            if "concrete" in material_name:
                if "cast" in material_name:
                    return "Cast Concrete"
                else:
                    return "Precast Concrete"
            else:
                return "Metal"

        return "No Material Found"


# Example usage:
ifc_path = "C:/Users/Костя/Downloads/Dummy_Detailed_Fixed.ifc"
line_number = 14559  # Example IFCBEAM line
extractor = IFCMaterialExtractor(ifc_path)
material_type = extractor.get_material_type(line_number)
print(f"The material type is: {material_type}")
