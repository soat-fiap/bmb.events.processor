from controllers.events_controller import EventsController
from use_cases.order import CreateOrderNodeUseCase
from use_cases.customer import CreateCustomerNodeUseCase
from use_cases.product import CreateProductNodeUseCase
from gateways.sqs import IntegrationQueueGateway
from gateways.neo4j_gateway import Neo4jGateway
import boto3
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

def main():

  NEO4J_URI = os.getenv('NEO4J_URI', 'neo4j+s://db5c9cae.databases.neo4j.io')
  NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
  NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'qDRQaOBpQBHFZB8XjF3pdnudUaI7-a3oIoMye2-CYwE')
  QUEUE_URL = os.getenv('QUEUE_URL', "https://sqs.us-east-1.amazonaws.com//boletimfocus")

  neo4j = Neo4jGateway(NEO4J_URI,NEO4J_USER, NEO4J_PASSWORD)
  integration_queue = IntegrationQueueGateway(boto3.client('sqs', region_name='us-east-1'), QUEUE_URL)
  
  with neo4j.get_driver() as neo4j_driver:
    print("Testing connection")
    neo4j_driver.verify_connectivity()
    
    create_order_use_case = CreateOrderNodeUseCase(neo4j_driver)
    create_product_use_case = CreateProductNodeUseCase(neo4j_driver)
    create_customer_use_case = CreateCustomerNodeUseCase(neo4j_driver)
  
    events_controller = EventsController(create_order_use_case, create_product_use_case, create_customer_use_case)
      
    for message in integration_queue.poll_messages():
      try:
        events_controller.process_message(message)
        integration_queue.delete_message(message)
      except Exception as e:
        print(f"Error processing message: {e}")

if __name__ == "__main__":
    main()