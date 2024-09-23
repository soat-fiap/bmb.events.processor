import json
from order_module import CreateOrderNodeUseCase
from customer_module import CreateCustomerNodeUseCase
from product_module import CreateProductNodeUseCase
from sqs import SqsService
from neo4j_service import Neo4jService
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

# Read environment variables
NEO4J_URI = os.getenv('NEO4J_URI', 'neo4j+s://935ee527.databases.neo4j.io')
NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'KwieHD-DlWsw7WhOLmrGAMqA-nkTedfOZqV8dp4BrBk')
QUEUE_URL = os.getenv('QUEUE_URL', "https://sqs.us-east-1.amazonaws.com//boletimfocus")
# AWS_API_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'neo4j')
# AWS_API_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'bk3AI_CP8USMsqc_9uf4YcoDEu1Bv5_cktZlY2tNY4s')

URI = NEO4J_URI
AUTH = (NEO4J_USER, NEO4J_PASSWORD)
print(f"Connecting to Neo4j at {NEO4J_URI} with user {NEO4J_USER} password {NEO4J_PASSWORD}")



sqs = boto3.client('sqs', region_name='us-east-1')

def map_usecase(event_type, neo4j_driver):
  print(f"Mapping event type: {event_type}")
  
  if event_type == "OrderCreated":
    return CreateOrderNodeUseCase(neo4j_driver)
  
  if event_type == "ProductCreated":
    return CreateProductNodeUseCase(neo4j_driver)
  
  if event_type == "CustomerRegistered":
    return CreateCustomerNodeUseCase(neo4j_driver)
  
  else:
    raise ValueError(f"Unknown event type: {event_type}")
  
def process_sqs_message(message, neo4j_driver):
  try:
    if message['MessageAttributes'] is not None:
      event_type = message['MessageAttributes'].get('EventType').get('StringValue')
      print(f"EventType: {event_type}")

      map_usecase(event_type, neo4j_driver).execute(read_json_from_string(message['Body']))
  except Exception as e:
    print(f"Error processing message: {e}")

def main():
  neo4j = Neo4jService(NEO4J_URI,NEO4J_USER, NEO4J_PASSWORD)
  sqs = SqsService(boto3.client('sqs', region_name='us-east-1'), QUEUE_URL)
  
  print("Testing connection")
  neo4j.get_driver().verify_connectivity()
    
  for message in sqs.poll_messages():
    try:
      process_sqs_message(message, neo4j.get_driver())
      sqs.delete_message(message)
    except Exception as e:
      print(f"Error processing message: {e}")

if __name__ == "__main__":
    main()