from flask import Flask, render_template, request
from query_handler import QueryHandler
from api import api_bp
import os
import atexit

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(api_bp, url_prefix='/api')

query_handler = QueryHandler()

@atexit.register
def close_driver_on_exit():
    query_handler.close_driver()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/display', methods=['GET'])
def display():
    try:
        algorithm = request.args.get('algorithm', 'louvain').lower()
        cluster_id = request.args.get('cluster')

        if not cluster_id:
            return render_template('display.html', error="Cluster ID is required.", algorithm=None, cluster_id=None, edges=[])

        if not algorithm:
            return render_template('display.html', error="Algorithm parameter is missing.", algorithm=None, cluster_id=None, edges=[])

        property_key = 'community' if algorithm == 'louvain' else 'component' if algorithm == 'wcc' else None
        if not property_key:
            return render_template('display.html', error="Unsupported algorithm. Use 'louvain' or 'wcc'.", algorithm=None, cluster_id=None, edges=[])

        edges, error_message = query_handler.get_edges(property_key, cluster_id)
        
        if error_message:
            return render_template('display.html', error=error_message, algorithm=algorithm, cluster_id=cluster_id, edges=[])

        return render_template(
            'display.html',
            edges=edges or [],
            cluster_id=cluster_id,
            algorithm=algorithm
        )
    except Exception as e:
        return render_template('display.html', error=f"An unexpected error occurred: {str(e)}", algorithm=None, cluster_id=None, edges=[])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
