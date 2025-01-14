from flask import request, jsonify
from . import api_bp
from ..query_handler import QueryHandler

queryHandler = QueryHandler()

@api_bp.route('/paths', methods=['GET'])
def get_paths():
    graph_name = 'wordGraph'
    start_word = request.args.get('start_word', '').strip()
    end_word = request.args.get('end_word', '').strip()

    if not start_word or not end_word:
        return jsonify({"error": "Please provide both start_word and end_word."}), 400

    start_id, end_id = queryHandler.get_ids(graph_name, start_word, end_word)

    if start_id is None or end_id is None:
        return jsonify({"error": "One or both specified nodes were not found."}), 404

    paths = queryHandler.find_shortest_path(graph_name, start_id, end_id)

    if not paths:
        return jsonify({"message": "No paths were found with the specified parameters.", "paths": []}), 200

    return jsonify({"paths": paths, "start_word": start_word, "end_word": end_word}), 200

@api_bp.route('/download/json', methods=['POST'])
def download_json():
    data = request.get_json()
    if not data or 'paths' not in data:
        return jsonify({"error": "No paths provided."}), 400

    paths_data = data['paths']
    return jsonify(paths_data), 200
