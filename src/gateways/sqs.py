class IntegrationQueueGateway:
    
    def __init__(self, sqs_client, queue_url):
        self.sqs_client = sqs_client
        self.queue_url = queue_url

    def poll_messages(self):
        try:
            response = self.sqs_client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10,
                MessageAttributeNames=['EventType']
            )

            messages = response.get('Messages', [])
            print(f"Received {len(messages)} messages from SQS")
            return messages

        except Exception as e:
            print(f"Error polling SQS messages: {e}")

    def delete_message(self, message):
        print(f"Deleting message: {message['MessageId']}")
        try:
            self.sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            print(f"Message deleteed: {message['MessageId']}")
        except Exception as e:
            print(f"Error deleting message: {e}")