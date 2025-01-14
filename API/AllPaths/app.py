from flask import Flask, render_template, request, redirect, url_for, flash
from query_handler import QueryHandler
from api import api_bp
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
queryHandler = QueryHandler()

app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_word = request.form.get('start_word', '').strip().lower()
        end_word = request.form.get('end_word', '').strip().lower()

        if not start_word or not end_word:
            flash("Please complete all fields.", "error")
            return redirect(url_for('index'))

        paths = queryHandler.find_all_paths(start_word, end_word)

        if not paths:
            flash("No paths were found with the specified parameters.", "info")

        formatted_routes = []
        for path in paths:
            nodes = [node["id"] for node in path.nodes]
            relationships = [rel.type for rel in path.relationships]
            formatted_routes.append({
                "nodes": nodes,
                "relationships": relationships
            })

        return render_template('index.html', paths=formatted_routes, 
                               start_word=start_word, 
                               end_word=end_word)
    
    return render_template('index.html')

@app.route('/display', methods=['GET'])
def display():
    start_word = request.args.get('start_word', '').strip().lower()
    end_word = request.args.get('end_word', '').strip().lower()

    if not start_word or not end_word:
        flash("Incomplete parameters for display.", "error")
        return redirect(url_for('index'))
    
    paths = queryHandler.find_all_paths(start_word, end_word)
    
    if not paths:
        flash("No routes found to display.", "info")
        return redirect(url_for('index'))
    
    top_paths = paths[:4]
    formatted_paths = []
    for path in top_paths:
        nodes = [{"data": {"id": node["id"], "label": node["id"]}} for node in path.nodes]
        edges = []
        for rel in path.relationships:
            edges.append({
                "data": {
                    "id": f"{rel.start_node.id}-{rel.end_node.id}",
                    "source": rel.start_node["id"],
                    "target": rel.end_node["id"],
                    "label": rel.type
                }
            })
        formatted_paths.append({"elements": nodes + edges})
    
    return render_template('display.html', paths=formatted_paths, start_word=start_word, end_word=end_word)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
