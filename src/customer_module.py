def create_customer_node(tx, data):
    print("creating customer node")

    query = (
        "MERGE (c:Customer {id: $customerId}) "
    )
    tx.run(query, customerId=data["Id"])
    
    print("customer node created")