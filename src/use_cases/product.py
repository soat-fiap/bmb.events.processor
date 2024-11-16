class CreateProductNodeUseCase:
    
    def __init__(self, database, logger):
        self.logger = logger
        self.database = database

    def execute(self, data):
        
        product_id = data.get('id')
        product_name = data.get('name')
        self.logger.log(f"Starting creation of product: ID = {product_id}, Name = {product_name}")
        self.database.save_product(data)
        self.logger.log(f"Successfully created product: ID = {product_id}, Name = {product_name}")