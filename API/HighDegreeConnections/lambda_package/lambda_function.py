from flask import Flask, jsonify, request
import boto3
import json

app = Flask(__name__)

lambda_client = boto3.client('lambda')

@app.route('/top-connected-nodes', methods=['GET'])
def invoke_lambda():
    try:
        limit = request.args.get('limit', 10)
        min_length = request.args.get('min_length', None)

        try:
            limit = int(limit)
        except ValueError:
            return jsonify({"error": "'limit' must be an integer"}), 400
        
        if min_length is not None:
            try:
                min_length = int(min_length)
            except ValueError:
                return jsonify({"error": "'min_length' must be an integer"}), 400

        payload = {"limit": limit}
        if min_length is not None:
            payload["min_length"] = min_length

        response = lambda_client.invoke(
            FunctionName='HighDegreeNodes',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        payload = response['Payload'].read()
        payload = json.loads(payload)
        body = json.loads(payload['body'])

        return jsonify(body), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
