class CreateProductNodeUseCase:
    
    def __init__(self, database, logger):
        self.logger = logger
        self.database = database

    def execute(self, data):
        product_id = data.get('Id')
        product_name = data.get('Name')
        self.logger.log(f"Starting creation of product: ID = {product_id}, Name = {product_name}")
        self.database.save_product(data)
        self.logger.log(f"Successfully created product: ID = {product_id}, Name = {product_name}")