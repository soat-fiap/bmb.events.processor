

import json

class EventsController:
    def __init__(self, create_order_use_case, create_product_use_case, create_customer_use_case, logger) -> None:
        self.create_order_use_case = create_order_use_case
        self.create_product_use_case = create_product_use_case
        self.create_customer_use_case = create_customer_use_case
        self.logger = logger

    def __map_usecase(self, event_type):
        self.logger.log(f"Mapping event type: {event_type}")
        
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
            self.logger.error(f"Error decoding JSON: {e}"),
            return None

    def process_message(self, message):
        try:
            if message["messageType"] is not None:
                event_type = message["messageType"][0].split(":")[-1]
                self.logger.log(f"EventType: {event_type}")

                self.__map_usecase(event_type,).execute(message['message'])
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            raise
        
