from flask import Flask, render_template, jsonify, request, redirect, url_for
from HighDegreeConnections.webpage.query_handler import QueryHandler
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
query_handler = QueryHandler()

@app.route('/')
def index():
    return render_template('index.html')

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
        
        body = query_handler.invoke_lambda(limit, min_length)
        return jsonify(body), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search-word', methods=['POST'])
def search_word():
    word = request.form['word']
    connections = query_handler.word_connections(word)
    return render_template('display.html', word=word, connections=connections)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084)
