import json, re, subprocess, sys, os
from flask import Flask, send_from_directory, request, jsonify

# Directorios base
BAZILIO_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.path.join(BAZILIO_DIR, "INDEX")
PROGRAMAS = os.path.join(BAZILIO_DIR, "programas")

COMANDO = [sys.executable, "bazilio.py", "programas/hello.bzl"]

PLANTILLA = '''### Un programa en Bazilio ###

Main |:
    <w> "Hello Bazilio"
    (:) {%s}
:|
'''

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory(INDEX_DIR, 'index.html')

# Ruta para servir archivos estáticos generados (como programas/hello.pdf, etc.)
@app.route('/programas/<path:filename>')
def servir_programas(filename):
    return send_from_directory(PROGRAMAS, filename)

@app.route('/generar', methods=['POST'])
def generar():
    datos = request.get_json() or {}
    notas = datos.get("notas", "").strip()

    if not notas or re.search(r'[{}"]', notas):
        return jsonify({"ok": False, "log": "Notas vacías o con caracteres no válidos."})

    os.makedirs(PROGRAMAS, exist_ok=True)

    with open(os.path.join(PROGRAMAS, "hello.bzl"), "w", encoding="utf-8") as f:
        f.write(PLANTILLA % notas)

    try:
        r = subprocess.run(COMANDO, capture_output=True, text=True, cwd=BAZILIO_DIR)
        return jsonify({"ok": r.returncode == 0, "log": (r.stdout + r.stderr).strip()})
    except Exception as e:
        return jsonify({"ok": False, "log": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Abriendo servidor en http://localhost:{port}")
    app.run(host='0.0.0.0', port=port)