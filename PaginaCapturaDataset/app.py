import os
import base64
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

CLASES = [
    "limon",
    "mango",
    "manzana",
    "melon",
    "naranja",
    "pepino",
    "pina",
    "platano",
    "sandia"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Se guardará fuera de la página, dentro de redneuronal/fotos_reales
FOTOS_DIR = os.path.join(BASE_DIR, "..", "redneuronal", "fotos_reales")


@app.route("/")
def index():
    return render_template("index.html", clases=CLASES)


@app.route("/guardar_foto", methods=["POST"])
def guardar_foto():
    data = request.json

    clase = data.get("clase")
    imagen_base64 = data.get("imagen")

    if clase not in CLASES:
        return jsonify({"error": "Clase no válida"}), 400

    if not imagen_base64:
        return jsonify({"error": "No se recibió imagen"}), 400

    carpeta_clase = os.path.join(FOTOS_DIR, clase)
    os.makedirs(carpeta_clase, exist_ok=True)

    imagen_base64 = imagen_base64.split(",")[1]
    imagen_bytes = base64.b64decode(imagen_base64)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    nombre_archivo = f"{clase}_{timestamp}.jpg"

    ruta_archivo = os.path.join(carpeta_clase, nombre_archivo)

    with open(ruta_archivo, "wb") as f:
        f.write(imagen_bytes)

    total = len([
        archivo for archivo in os.listdir(carpeta_clase)
        if archivo.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    return jsonify({
        "mensaje": "Foto guardada correctamente",
        "archivo": nombre_archivo,
        "clase": clase,
        "total_clase": total
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)