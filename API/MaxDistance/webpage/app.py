from flask import Flask, render_template, request
from query_handler import QueryHandler

app = Flask(__name__)
query_handler = QueryHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    start_word = request.form.get('start_word')
    end_word = request.form.get('end_word')
    mode = request.form.get('mode')
    max_depth = request.form.get('max_depth', 10)

    if not start_word or not end_word:
        return render_template('index.html', error="Both start_word and end_word are required.")

    try:
        result = query_handler.invoke_lambda(start_word, end_word, mode, int(max_depth))
        return render_template('results.html', result=result)
    except Exception as e:
        return render_template('index.html', error=f"Error calling Lambda: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086)
