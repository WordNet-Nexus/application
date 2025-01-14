from flask import Flask, jsonify, render_template
import os
from query_handler import QueryHandler

app = Flask(__name__)
app.secret_key = os.urandom(24)
query_handler = QueryHandler()

@app.route('/isolated-nodes', methods=['GET'])
def invoke_lambda():
    try:
        body = query_handler.invoke_lambda()
        return jsonify(body), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)
