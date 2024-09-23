category_mapping = {
    0: "Meal",
    1: "Sides",
    2: "Drink",
    3: "Dessert",
}

class CreateProductNodeUseCase:
    
    def __init__(self, driver):
        self.driver = driver

    def __create_node(self, tx, data):
        print("creating product node")
    
        query = (
            "MERGE (p:Product {id: $product_id, name: $name, category: $category, price: $price}) "
        )
        tx.run(query, product_id=data["Id"], name=data["Name"], category=category_mapping[data["Category"]], price=data["Price"])
        
        print("product node created")
        
    def execute(self, data):
        with self.driver.session(database="neo4j") as session:
            print("saving on neo4j")
            session.execute_write(self.__create_node, data)