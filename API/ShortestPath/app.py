from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import json
import os
from ShortestPath.query_handler import QueryHandler
from api import api_bp

app = Flask(__name__)
app.secret_key = os.urandom(24)
queryHandler = QueryHandler()

app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start_word = request.form.get('start_word', '').strip()
        end_word = request.form.get('end_word', '').strip()

        if not start_word or not end_word:
            flash("Please fill out all fields.", "error")
            return redirect(url_for('index'))

        start_id, end_id = queryHandler.get_ids('wordGraph', start_word, end_word)

        if start_id is None or end_id is None:
            flash("One or both of the specified nodes were not found.", "error")
            return redirect(url_for('index'))

        paths = queryHandler.find_shortest_path('wordGraph', start_id, end_id)
        if not paths:
            flash("No paths were found with the specified parameters.", "info")

        return render_template('index.html', paths=paths, 
                               start_word=start_word, 
                               end_word=end_word)
    
    return render_template('index.html')

@app.route('/download/json', methods=['POST'])
def download_json():
    paths = request.form.get('paths')
    if not paths:
        return "No paths were provided.", 400

    paths_data = json.loads(paths)
    response = make_response(json.dumps(paths_data, indent=4))
    response.headers["Content-Disposition"] = "attachment; filename=path.json"
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
