import json

class ProductMapper:
    def __init__(self, json_file="analyser/product_mapping_schema.json"):
        with open(json_file, "r") as file:
            self.product_mapping_schema = json.load(file)

    def find_product(self, instance1, instance2, material1, material2):
        try:
            product = self.product_mapping_schema[instance1][material1][instance2][material2]
            return product
        except KeyError:
            return None

# Example usage
finder = ProductMapper()
product = finder.find_product("column", "beam", "concrete", "metal")
print(product)  # Expected Output: ["Weilda", "Threlda"]
