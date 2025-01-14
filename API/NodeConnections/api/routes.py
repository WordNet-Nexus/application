from flask import request, jsonify
from . import api_bp
from ..query_handler import QueryHandler

query_handler = QueryHandler()

def create_json_response(status, data=None, message=None):
    response = {"status": status}
    if data is not None:
        response["data"] = data
    elif message is not None:
        response["message"] = message
    return jsonify(response)

@api_bp.route('/nodes/specific_degree', methods=['GET'])
def get_nodes_with_specific_degree():
    try:
        degree = int(request.args.get('degree'))
        nodes = query_handler.get_nodes_by_degree(degree)
        return create_json_response("success", data=nodes), 200
    except (ValueError, TypeError):
        return create_json_response("error", message="Invalid or missing 'degree' parameter."), 400
    except Exception as e:
        return create_json_response("error", message=str(e)), 500

@api_bp.route('/nodes/degree_range', methods=['GET'])
def get_nodes_with_degree_range():
    try:
        min_degree = int(request.args.get('min_degree'))
        max_degree = int(request.args.get('max_degree'))

        if min_degree > max_degree:
            return create_json_response("error", message="'min_degree' cannot be greater than 'max_degree'."), 400
        nodes = query_handler.get_nodes_by_degree_range(min_degree, max_degree)
        return create_json_response("success", data=nodes), 200
    except (ValueError, TypeError):
        return create_json_response("error", message="Invalid or missing 'min_degree' and 'max_degree' parameters."), 400
    except Exception as e:
        return create_json_response("error", message=str(e)), 500

@api_bp.route('/nodes/min_degree', methods=['GET'])
def get_nodes_with_min_degree():
    try:
        min_degree = int(request.args.get('min_degree'))
        nodes = query_handler.get_nodes_by_min_degree(min_degree)
        return create_json_response("success", data=nodes), 200
    except (ValueError, TypeError):
        return create_json_response("error", message="Invalid or missing 'min_degree' parameter."), 400
    except Exception as e:
        return create_json_response("error", message=str(e)), 500
