from relations_module import create_customer_order_relationship, create_order_items_relationship

class CreateOrderNodeUseCase:
    
    def __init__(self, driver):
        self.driver = driver

    def create_order_node(self, tx, order_id):
        print(f'creating order node: {order_id}')
        query = (
            "MERGE (o:Order {id: $order_id}) "
        )
        tx.run(query, order_id=order_id)
        
        print(f"order {order_id} node created")
        
    def execute(self, order_created):
        with self.driver.session(database="neo4j") as session:
            print("saving on neo4j")
            order_id = order_created["Id"]
            session.execute_write(self.create_order_node, order_id)
      
            if order_created["Customer"] is not None:
              session.execute_write(create_customer_order_relationship, order_created["Id"], order_created["Customer"]["Id"])
            
            session.execute_write(create_order_items_relationship, order_created["OrderItems"])
