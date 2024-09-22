def create_customer_order_relationship(tx, orderId, customerId):
    print("creating customer-order relationship")
    
    query = (
        "MERGE (o:Order {id: $orderId}) "
        "MERGE (c:Customer {id: $customerId}) "
        "MERGE (c)-[:PLACED]->(o)"
    )
    tx.run(query, orderId=orderId, customerId=customerId)
    
    print("customer-order relationship created")

def create_order_item_relationship(tx, order_id, product_id):
    print("creating order-item relationship")

    query = (
        "MERGE (o:Order {id: $order_id}) "
        "MERGE (p:Product {id: $product_id}) "
        "MERGE (o)-[:CONTAINS]->(p)"
    )
    tx.run(query, order_id=order_id, product_id=product_id)

    print("order-item relationship created")

def create_order_items_relationship(tx, order_items):
    print("creating order-items relationships")

    for order_item in order_items:
        create_order_item_relationship(tx, order_item["OrderId"], order_item["ProductId"])

    print("order-items relationships created")