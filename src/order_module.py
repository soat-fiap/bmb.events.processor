
def create_order_node(tx, orderId):
    print("creating order node")
    
    query = (
        "MERGE (o:Order {id: $orderId}) "
    )
    tx.run(query, orderId=orderId)
    
    print("order node created")