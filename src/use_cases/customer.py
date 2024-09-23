class CreateCustomerNodeUseCase:
    
    def __init__(self, driver):
        self.driver = driver

    def create_customer_node(self, tx, data):
        print("creating customer node")

        query = (
            "MERGE (c:Customer {id: $customerId}) "
        )
        tx.run(query, customerId=data["Id"])
        
        print("customer node created")
        
    def execute(self, data):
        with self.driver.session(database="neo4j") as session:
            print("saving on neo4j")
            session.execute_write(self.create_customer_node, data)