from flask import request, jsonify
from ..query_handler import QueryHandler
from . import api_bp

query_handler = QueryHandler()

def display_results(response, error_message):
    if error_message:
        return jsonify({
            "status": "error",
            "message": error_message
        }), 400

    return jsonify({
        "status": "success",
        "data": response
    }), 200

@api_bp.route('/clusters', methods=['GET'])
def clusters():
    algorithm = request.args.get('algorithm', 'louvain').lower()
    response, error_message = query_handler.detect_clusters(algorithm)
    return display_results(response, error_message)

@api_bp.route('/clusters/results', methods=['GET'])
def get_cluster_results():
    property_key = request.args.get('property', 'community')
    nodes, error_message = query_handler.fetch_cluster_results(property_key)
    return display_results(nodes, error_message)

@api_bp.route('/download/all_results', methods=['GET'])
def download_all_results():
    property_key = request.args.get('property', 'community')
    nodes, error_message = query_handler.fetch_cluster_results(property_key)
    return display_results(nodes, error_message)

@api_bp.route('/download/cluster', methods=['GET'])
def download_cluster():
    algorithm = request.args.get('algorithm', 'louvain').lower()
    cluster_id = request.args.get('cluster')
    property_key = 'community' if algorithm == 'louvain' else 'component' if algorithm == 'wcc' else None

    if not property_key or not cluster_id:
        return jsonify({
            "status": "error",
            "message": "Cluster ID and algorithm are required."
        }), 400
    edges, error_message = query_handler.get_edges(property_key, cluster_id)
    return display_results(edges, error_message)
