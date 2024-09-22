category_mapping = {
    0: "Meal",
    1: "Sides",
    2: "Drink",
    3: "Dessert",
}

def create_product_node(tx, data):
    print("creating product node")
    
    query = (
        "MERGE (p:Product {id: $productId, name: $name, category: $category, price: $price}) "
    )
    tx.run(query, productId=data["Id"], name=data["Name"], category=category_mapping[data["Category"]], price=data["Price"])
    
    print("product node created")