from flask import request, jsonify, make_response
from . import api_bp
from query_handler import QueryHandler

queryHandler = QueryHandler()

@api_bp.route('/paths', methods=['GET'])
def get_paths():
    start_word = request.args.get('start_word', '').strip().lower()
    end_word = request.args.get('end_word', '').strip().lower()

    if not start_word or not end_word:
        return jsonify({"error": "Please provide both start_word and end_word."}), 400

    paths = queryHandler.find_all_paths(start_word, end_word)

    if not paths:
        return jsonify({"message": "No paths were found with the specified parameters.", "paths": []}), 200

    formatted_routes = []
    for path in paths:
        nodes = [node["id"] for node in path.nodes]
        relationships = [rel.type for rel in path.relationships]
        formatted_routes.append({
            "nodes": nodes,
            "relationships": relationships
        })

    return jsonify({"paths": formatted_routes, "start_word": start_word, "end_word": end_word}), 200

@api_bp.route('/download', methods=['GET'])
def download():
    start_word = request.args.get('start_word', '').strip().lower()
    end_word = request.args.get('end_word', '').strip().lower()

    if not start_word or not end_word:
        return jsonify({"error": "Please provide both start_word and end_word."}), 400

    paths = queryHandler.find_all_paths(start_word, end_word)

    if not paths:
        return jsonify({"error": "No paths were found with the specified parameters."}), 404

    formatted_routes = []
    for path in paths:
        nodes = [node["id"] for node in path.nodes]
        relationships = [rel.type for rel in path.relationships]
        formatted_routes.append({
            "nodes": nodes,
            "relationships": relationships
        })

    data = {
        "start_word": start_word,
        "end_word": end_word,
        "paths": formatted_routes
    }

    response = make_response(jsonify(data))
    response.headers['Content-Disposition'] = f'attachment; filename=paths_{start_word}_to_{end_word}.json'
    response.headers['Content-Type'] = 'application/json'
    return response
