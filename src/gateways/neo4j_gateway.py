from neo4j import GraphDatabase

category_mapping = {
    0: "Meal",
    1: "Sides",
    2: "Drink",
    3: "Dessert",
}

class Neo4jGateway:

    def __init__(self, uri, user, password, logger):
        self.logger = logger
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()
        self.logger.log("Neo4j driver initialized")

    def get_driver(self):
        return self.driver    

    def save_customer(self, customer_data):
        query = (
            "MERGE (c:Customer {id: $customer_id}) "
        )
        self.logger.log(f"Saving customer with ID: {customer_data['Id']}")
        self.__execute(query, customer_id=customer_data["Id"])

    def save_product(self, product_data):
        query = (
            "MERGE (p:Product {id: $product_id, name: $name, category: $category}) "
        )
        self.logger.log(f"Saving product with ID: {product_data['id']}, Name: {product_data['name']}")
        self.__execute(query, product_id=product_data["id"], name=product_data["name"], category=product_data["category"])

    def save_order(self, order):
        query = (
            "MERGE (o:Order {id: $order_id}) "
        )
        self.logger.log(f"Saving order with ID: {order['id']}")
        self.__execute(query, order_id=order["id"])

    def save_customer_order_relationship(self, order):
        query = (
            "MERGE (o:Order {id: $order_id}) "
            "MERGE (c:Customer {id: $customer_id}) "
            "MERGE (c)-[:PLACED]->(o)"
        )
        self.logger.log(f"Creating relationship between customer ID: {order['customer']['id']} and order ID: {order['id']}")
        self.__execute(query, order_id=order["id"], customer_id=order["customer"]["id"])

    def __create_order_item_relationship(self, order_item):
        query = (
            "MERGE (o:Order {id: $order_id}) "
            "MERGE (p:Product {id: $product_id}) "
            "MERGE (o)-[:CONTAINS]->(p)"
        )
        self.logger.log(f"Creating relationship between order ID: {order_item['orderId']} and product ID: {order_item['id']}")
        self.__execute(query, order_id=order_item["orderId"], product_id=order_item["id"])

    def save_product_order_relationship(self, order_item):
        self.__create_order_item_relationship(order_item)

    def __run_transaction(self, tx, query, **data):
        self.logger.log(f"Executing transaction with query: {query} and data: {data}")
        tx.run(query, **data)

    def __execute(self, query, **params):
        self.logger.log("Preparing Neo4j session")
        with self.driver.session(database="neo4j") as session:
            self.logger.log(f"Executing query: {query} with params: {params}")
            session.execute_write(self.__run_transaction, query, **params)