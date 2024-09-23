category_mapping = {
    0: "Meal",
    1: "Sides",
    2: "Drink",
    3: "Dessert",
}

class CreateProductNodeUseCase:
    
    def __init__(self, driver):
        self.driver = driver

    def create_product_node(self, tx, data):
        print("creating product node")
    
        query = (
            "MERGE (p:Product {id: $productId, name: $name, category: $category, price: $price}) "
        )
        tx.run(query, productId=data["Id"], name=data["Name"], category=category_mapping[data["Category"]], price=data["Price"])
        
        print("product node created")
        
    def execute(self, data):
        with self.driver.session(database="neo4j") as session:
            print("saving on neo4j")
            session.execute_write(self.create_product_node, data)