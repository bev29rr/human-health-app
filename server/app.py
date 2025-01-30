from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__, static_url_path='/static')

TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'

@app.route('/<filename>.html')
def serve_html(filename):
    try:
        return send_from_directory(TEMPLATES_DIR, f'{filename}.html')
    except FileNotFoundError:
        return f"El archivo {filename}.html no se encuentra disponible", 404

@app.route('/static/css/<filename>')
def serve_css(filename):
    try:
        return send_from_directory(os.path.join(STATIC_DIR, 'css'), filename)
    except FileNotFoundError:
        return f"Archivo CSS {filename} no encontrado", 404

# Ruta dinámica para servir archivos JS
@app.route('/static/js/<filename>')
def serve_js(filename):
    try:
        return send_from_directory(os.path.join(STATIC_DIR, 'js'), filename)
    except FileNotFoundError:
        return f"Archivo JS {filename} no encontrado", 404

@app.route('/')
def index():
    return send_from_directory(TEMPLATES_DIR, 'index.html')

if __name__ == '__main__':
    app.run(debug=False)
