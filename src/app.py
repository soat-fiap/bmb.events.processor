from custom_logger import Logger
from controllers.events_controller import EventsController
from use_cases.order import CreateOrderNodeUseCase
from use_cases.customer import CreateCustomerNodeUseCase
from use_cases.product import CreateProductNodeUseCase
from gateways.sqs import IntegrationQueueGateway
from gateways.neo4j_gateway import Neo4jGateway
import boto3
import os
import json

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
  "messageId": "645f0000-9742-806d-578d-08dd05cdde27",
  "requestId": null,
  "correlationId": null,
  "conversationId": "645f0000-9742-806d-583b-08dd05cdde27",
  "initiatorId": null,
  "sourceAddress": "amazonsqs://us-east-1/ITALOQ_FIAPTechChallengeByteMeBurgerApi_bus_ctxoyyrzekyg595wbdqomt1und?durable=false&autodelete=true",
  "destinationAddress": "amazonsqs://us-east-1/Bmb_Domain_Core_Events_Integration-ProductCreated?type=topic",
  "responseAddress": null,
  "faultAddress": null,
  "messageType": [
    "urn:message:Bmb.Domain.Core.Events.Integration:ProductCreated",
    "urn:message:Bmb.Domain.Core.Events.Integration:IBmbIntegrationEvent"
  ],
  "message": {
    "id": "32c640c4-0aba-4580-a0a1-270e376ccc68",
    "name": "HAMBURGUER",
    "category": "Meal"
  },
  "expirationTime": null,
  "sentTime": "2024-11-15T23:33:11.0033293Z",
  "headers": {},
  "host": {
    "machineName": "ITALOQ",
    "processName": "FIAP.TechChallenge.ByteMeBurger.Api",
    "processId": 24420,
    "assembly": "FIAP.TechChallenge.ByteMeBurger.Api",
    "assemblyVersion": "1.0.0.0",
    "frameworkVersion": "8.0.3",
    "massTransitVersion": "8.2.5.0",
    "operatingSystemVersion": "Microsoft Windows NT 10.0.22631.0"
  }
}"""

json_order_created= """
{
  "messageId": "645f0000-9742-806d-1146-08dd05d22215",
  "requestId": null,
  "correlationId": null,
  "conversationId": "645f0000-9742-806d-3136-08dd05d22215",
  "initiatorId": null,
  "sourceAddress": "amazonsqs://us-east-1/ITALOQ_FIAPTechChallengeByteMeBurgerApi_bus_ctxoyyrzekyg595wbdqomt1und?durable=false&autodelete=true",
  "destinationAddress": "amazonsqs://us-east-1/Bmb_Domain_Core_Events_Integration-OrderCreated?type=topic",
  "responseAddress": null,
  "faultAddress": null,
  "messageType": [
    "urn:message:Bmb.Domain.Core.Events.Integration:OrderCreated",
    "urn:message:Bmb.Domain.Core.Events.Integration:IBmbIntegrationEvent"
  ],
  "message": {
    "id": "eb78ec69-e8f8-4198-9b7a-fe64f128cb12",
    "customer": null,
    "items": [
      {
        "id": "eb78ec69-e8f8-4198-9b7a-fe64f128cb12",
        "orderId": "eb78ec69-e8f8-4198-9b7a-fe64f128cb12",
        "productName": "HAMBURGUER",
        "unitPrice": "12.00",
        "quantity": 2
      },
      {
        "id": "eb78ec69-e8f8-4198-9b7a-fe64f128cb12",
        "orderId": "eb78ec69-e8f8-4198-9b7a-fe64f128cb12",
        "productName": "DOCE DE LEITE",
        "unitPrice": "5.00",
        "quantity": 2
      },
      {
        "id": "eb78ec69-e8f8-4198-9b7a-fe64f128cb12",
        "orderId": "eb78ec69-e8f8-4198-9b7a-fe64f128cb12",
        "productName": "H20",
        "unitPrice": "7.50",
        "quantity": 2
      },
      {
        "id": "eb78ec69-e8f8-4198-9b7a-fe64f128cb12",
        "orderId": "eb78ec69-e8f8-4198-9b7a-fe64f128cb12",
        "productName": "BATATA FRINTA",
        "unitPrice": "8.70",
        "quantity": 1
      }
    ],
    "status": 0,
    "orderTrackingCode": "A6U-94E",
    "paymentId": null,
    "total": "57.70"
  },
  "expirationTime": null,
  "sentTime": "2024-11-16T00:03:42.9555526Z",
  "headers": {},
  "host": {
    "machineName": "ITALOQ",
    "processName": "FIAP.TechChallenge.ByteMeBurger.Api",
    "processId": 24420,
    "assembly": "FIAP.TechChallenge.ByteMeBurger.Api",
    "assemblyVersion": "1.0.0.0",
    "frameworkVersion": "8.0.3",
    "massTransitVersion": "8.2.5.0",
    "operatingSystemVersion": "Microsoft Windows NT 10.0.22631.0"
  }
}
"""

def main():

    NEO4J_URI = os.getenv('NEO4J_URI', 'neo4j+s://x.databases.neo4j.io')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
    QUEUE_URL = os.getenv('QUEUE_URL', "https://sqs.us-east-1.amazonaws.com//events-processor")

    logger = Logger()
    neo4j = Neo4jGateway(NEO4J_URI,NEO4J_USER, NEO4J_PASSWORD, logger)
    integration_queue = IntegrationQueueGateway(boto3.client('sqs', region_name='us-east-1'), QUEUE_URL, logger)
  
    
    create_order_use_case = CreateOrderNodeUseCase(neo4j, logger)
    create_product_use_case = CreateProductNodeUseCase(neo4j, logger)
    create_customer_use_case = CreateCustomerNodeUseCase(neo4j, logger)

    events_controller = EventsController(create_order_use_case, create_product_use_case, create_customer_use_case, logger)
        
    for message in integration_queue.poll_messages():
        try:
            events_controller.process_message(json.loads(message.get('Body')))
            integration_queue.delete_message(message)
        except Exception as e:
            logger.log(f"Error processing message: {e}")

if __name__ == "__main__":
    main()