class CreateCustomerNodeUseCase:
    
    def __init__(self, driver):
        self.driver = driver

    def __create_node(self, tx, data):
        print("creating customer node")

        query = (
            "MERGE (c:Customer {id: $customer_id}) "
        )
        tx.run(query, customer_id=data["Id"])
        
        print("customer node created")
        
    def execute(self, data):
        with self.driver.session(database="neo4j") as session:
            print("saving on neo4j")
            session.execute_write(self.__create_node, data)