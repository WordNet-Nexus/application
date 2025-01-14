import boto3
import json

class QueryHandler:

    def __init__(self):
        self.lambda_client = boto3.client('lambda')
    
    def invoke_lambda(self):
        response = self.lambda_client.invoke(
            FunctionName='IsolatedNodes',
            InvocationType='RequestResponse'
        )

        payload = response['Payload'].read()
        payload = json.loads(payload)
        body = json.loads(payload['body'])

        return body