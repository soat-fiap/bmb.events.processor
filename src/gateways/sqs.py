class IntegrationQueueGateway:
    
    def __init__(self, sqs_client, queue_url, logger):
        self.logger = logger
        self.sqs_client = sqs_client
        self.queue_url = queue_url

    def poll_messages(self):
        try:
            self.logger.log("Polling messages from SQS queue...")
            response = self.sqs_client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10,
                MessageAttributeNames=['EventType']
            )

            messages = response.get('Messages', [])
            self.logger.log(f"Successfully received {len(messages)} messages from SQS queue: {self.queue_url}")
            return messages

        except Exception as e:
            self.logger.log(f"Error polling SQS messages from queue {self.queue_url}: {e}")

    def delete_message(self, message):
        message_id = message.get('MessageId', 'Unknown')
        self.logger.log(f"Attempting to delete message with ID: {message_id}")
        try:
            self.sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            self.logger.log(f"Successfully deleted message with ID: {message_id} from queue: {self.queue_url}")
        except Exception as e:
            self.logger.log(f"Error deleting message with ID: {message_id} from queue {self.queue_url}: {e}")