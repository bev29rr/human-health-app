import jinja2
from flask import Flask, send_from_directory, render_template, request, jsonify
import os

app = Flask(__name__, static_url_path='/static')

TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'

def read_file(file_path):
    try:
        with open(f"static/txt/{file_path}", 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except IOError:
        return f"Error: There was an issue reading the file '{file_path}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@app.route('/login', methods=['POST'])
def handle_message():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    print(f"Received message: {username}")
    
    return jsonify({"response": True})

@app.route('/<filename>.html')
def serve_html(filename):
    try:
        return render_template(f'{filename}.html')
    except jinja2.exceptions.TemplateNotFound:
        return jsonify({"error": f"Template {filename}.html not found."}), 40

@app.route('/static/css/<filename>')
def serve_css(filename):
    try:
        return send_from_directory(os.path.join(STATIC_DIR, 'css'), filename)
    except FileNotFoundError:
        return f"The CSS file {filename} isn't available", 404

@app.route('/static/js/<filename>')
def serve_js(filename):
    try:
        return send_from_directory(os.path.join(STATIC_DIR, 'js'), filename)
    except FileNotFoundError:
        return f"The JS file {filename} isn't available", 404

@app.route('/')
def index():
    text_contents = read_file("about.txt")
    return render_template('index.html', about_text=text_contents)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Page not found", "message": "The requested URL was not found on the server."}), 404

if __name__ == '__main__':
    app.run(debug=False)
