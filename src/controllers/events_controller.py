

import json

class EventsController:
    def __init__(self, create_order_use_case, create_product_use_case, create_customer_use_case) -> None:
        self.create_order_use_case = create_order_use_case
        self.create_product_use_case = create_product_use_case
        self.create_customer_use_case = create_customer_use_case

    def __map_usecase(self, event_type):
        print(f"Mapping event type: {event_type}")
        
        use_case_mapping = {
            "OrderCreated": self.create_order_use_case,
            "ProductCreated": self.create_product_use_case,
            "CustomerRegistered": self.create_customer_use_case
        }
        
        if event_type in use_case_mapping:
            return use_case_mapping[event_type]
        else:
            raise ValueError(f"Unknown event type: {event_type}")
        
    def __read_json_from_string(self, json_string):
        try:
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}"),
            return None

    def process_message(self, message):
        try:
            if message['MessageAttributes'] is not None:
                event_type = message['MessageAttributes'].get('EventType').get('StringValue')
                print(f"EventType: {event_type}")

                self.__map_usecase(event_type,).execute(self.__read_json_from_string(message['Body']))
        except Exception as e:
            print(f"Error processing message: {e}")
            raise
        
