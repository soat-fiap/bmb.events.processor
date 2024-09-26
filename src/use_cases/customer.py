class CreateCustomerNodeUseCase:
    
    def __init__(self, database, logger):
        self.logger = logger
        self.database = database

    def execute(self, data):
        customer_id = data.get('Id')
        customer_name = data.get('Name')
        
        self.logger.log(f"Starting creation of customer: ID = {customer_id}, Name = {customer_name}")
        self.database.save_customer(data)
        self.logger.log(f"Successfully created customer: ID = {customer_id}, Name = {customer_name}")