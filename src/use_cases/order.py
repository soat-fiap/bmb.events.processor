class CreateOrderNodeUseCase:
    
    def __init__(self, database, logger):
        self.logger = logger
        self.database = database

    def __create_order(self, order):
        self.logger.log(f'Starting creation of order: ID = {order["id"]}')
        self.database.save_order(order)
        self.logger.log(f'Order created: ID = {order["id"]}')
        
    def __create_customer_order_relationship(self, order):
        self.logger.log(f'Starting creation of customer-order relationship: Order ID = {order["id"]}, Customer ID = {order["customer"]["id"]}')
        self.database.save_customer_order_relationship(order)
        self.logger.log(f'Customer-order relationship created: Order ID = {order["id"]}, Customer ID = {order["customer"]["id"]}')
        
    def __create_product_relationship(self, order_items):
        for item in order_items:
            self.logger.log(f'Starting creation of product-order relationship: Order ID = {item["orderId"]}, Product ID = {item["id"]}, Product Name = {item["productName"]}')
            self.database.save_product_order_relationship(item)
            self.logger.log(f'Product-order relationship created: Order ID = {item["orderId"]}, Product ID = {item["id"]}, Product Name = {item["productName"]}')
        
    def execute(self, order_created):
        self.__create_order(order_created)
      
        if order_created["customer"] is not None:
            self.__create_customer_order_relationship(order_created)
            
        self.__create_product_relationship(order_created["items"])
