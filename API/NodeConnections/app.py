from flask import Flask, render_template
from .api import api_bp
import atexit
from .query_handler import QueryHandler

app = Flask(__name__)
query_handler = QueryHandler()

app.register_blueprint(api_bp, url_prefix='/api')

@atexit.register
def close_driver_on_exit():
    query_handler.close_driver()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)
