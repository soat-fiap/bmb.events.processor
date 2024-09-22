import json
from neo4j import GraphDatabase
from order_module import create_order_node
from customer_module import create_customer_node
from product_module import create_product_node
from relations_module import create_customer_order_relationship, create_order_items_relationship
import boto3
import uuid
import os

json_string_customer = """
{
    "Cpf": {
        "Value": "11068403055"
    },
    "Name": "110.684.030-55",
    "Email": "user@example.com",
    "Id": "d9969017-e152-4ba2-a3c6-d1149be9fb7d",
    "Created": "0001-01-01T00:00:00",
    "Updated": null
}
"""

json_string_product = """
{
    "Name": "234234234",
    "Description": "STRING",
    "Category": 0,
    "Price": 30,
    "Images": [
        "string"
    ],
    "Id": "e8fe73be-4587-41f6-81fb-be2e09075a17",
    "Created": "2024-09-21T18:47:56.1511079Z",
    "Updated": null
}
"""

json_order_created= """
{
    "Customer": {
        "Id": "d9969017-e152-4ba2-a3c6-d1149be9fb7d"
    },
    "TrackingCode": {
        "Value": "RK-B66"
    },
    "Status": 0,
    "OrderItems": [
        {
            "OrderId": "3438cd57-7341-4cf2-8d90-4055396b622c",
            "ProductId": "ab2697a9-9b1c-4714-8806-e419a7153c9b",
            "ProductName": "234234234",
            "UnitPrice": 30,
            "Quantity": 2,
            "Id": "1b9b8184-c15e-49a6-aa9a-1dfb3bb6d743",
            "Created": "0001-01-01T00:00:00",
            "Updated": null
        }
    ],
    "Total": 60,
    "PaymentId": null,
    "Id": "3438cd57-7341-4cf2-8d90-4055396b622c",
    "Created": "2024-09-21T18:54:21.1015035Z",
    "Updated": null
}
"""

def read_json_from_string(json_string):
    try:
        json_data = json.loads(json_string)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}"),
        return None

def exec_query(driver, func, *data):
  with driver.session(database="neo4j") as session:
    session.execute_write(func, *data)

# Read environment variables
NEO4J_URI = os.getenv('NEO4J_URI', '-neo4j+s://5a219891.databases.neo4j.io')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'bk3AI_CP8USMsqc_9uf4YcoDEu1Bv5_cktZlY2tNY4s')
# AWS_API_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'neo4j')
# AWS_API_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'bk3AI_CP8USMsqc_9uf4YcoDEu1Bv5_cktZlY2tNY4s')

URI = NEO4J_URI
AUTH = (NEO4J_USER, NEO4J_PASSWORD)
print(f"Connecting to Neo4j at {NEO4J_URI} with user {NEO4J_USER} password {NEO4J_PASSWORD}")

# with GraphDatabase.driver(URI, auth=AUTH) as driver:

#     product = read_json_from_string(json_string_product)
#     product["Id"] = str(uuid.uuid4())
#     order = read_json_from_string(json_order_created)
#     order["Id"] = str(uuid.uuid4())
#     order["OrderItems"][0]["OrderId"] = order["Id"]
#     order["OrderItems"][0]["ProductId"] = product["Id"]
#     customer = read_json_from_string(json_string_customer)

#     print("Testing connection")
#     driver.verify_connectivity()
    
#     print("Creating nodes and relationships")

#     exec_query(driver, create_order_node, order["Id"])
#     exec_query(driver, create_product_node, product)
#     exec_query(driver, create_customer_node, customer)
#     if order["Customer"] is not None:
#         exec_query(driver, create_customer_order_relationship, order["Id"], order["Customer"]["Id"])
#     exec_query(driver, create_order_items_relationship, order["OrderItems"])
    

#     print("Nodes and relationships created")

#     # Initialize SQS client
sqs = boto3.client('sqs', region_name='us-east-1')

#     # # URL of the SQS queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/0000/boletimfocus'

def poll_sqs_messages():
    try:
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
            MessageAttributeNames=['EventType']
        )

        messages = response.get('Messages', [])
        for message in messages:
            if message['MessageAttributes'] is not None:
                event_type = message['MessageAttributes'].get('EventType').get('StringValue')
                print(f"EventType: {event_type}")
                print(f"Received message: {message["Body"]}")

            # Delete the message from the queue after processing
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            print(f"Deleted message: {message['MessageId']}")

    except Exception as e:
        print(f"Error polling SQS messages: {e}")

# Poll messages from SQS
poll_sqs_messages()