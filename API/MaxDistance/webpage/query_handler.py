import boto3
import json

class QueryHandler:
    def __init__(self):
        self.lambda_client = boto3.client('lambda')

    def invoke_lambda(self, start_word, end_word, mode="steps", max_depth=10):
        payload = {
            "start_word": start_word,
            "end_word": end_word,
            "mode": mode,
            "max_depth": max_depth
        }
        response = self.lambda_client.invoke(
            FunctionName='MaxDistance',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        response_payload = response['Payload'].read()
        response_payload = json.loads(response_payload)
        if "body" in response_payload:
            body = json.loads(response_payload["body"])
        else:
            body = response_payload

        return body
