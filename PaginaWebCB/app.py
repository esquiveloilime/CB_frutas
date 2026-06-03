import base64
import io
import os

import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, jsonify
from PIL import Image

app = Flask(__name__)

IMG_SIZE = 100
MODEL_PATH = "modelo/mejor_modelo.keras"
CLASSES_PATH = "modelo/clases.txt"

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]


frutas_info = {
    "manzana": {
        "precio": 42.90,
        "unidad": "kg",
        "descripcion": "La manzana es rica en fibra y antioxidantes."
    },
    "platano": {
        "precio": 24.90,
        "unidad": "kg",
        "descripcion": "El plátano aporta potasio y energía."
    },
    "naranja": {
        "precio": 29.90,
        "unidad": "kg",
        "descripcion": "La naranja contiene vitamina C."
    },
    "limon": {
        "precio": 34.90,
        "unidad": "kg",
        "descripcion": "El limón es usado por su acidez y vitamina C."
    },
    "pepino": {
        "precio": 26.90,
        "unidad": "kg",
        "descripcion": "El pepino tiene alto contenido de agua."
    },
    "durazno": {
        "precio": 59.90,
        "unidad": "kg",
        "descripcion": "El durazno contiene vitaminas A y C."
    },
    "kiwi": {
        "precio": 89.90,
        "unidad": "kg",
        "descripcion": "El kiwi es rico en vitamina C y fibra."
    },
    "sandia": {
        "precio": 18.90,
        "unidad": "kg",
        "descripcion": "La sandía es refrescante y contiene mucha agua."
    },
    "pina": {
        "precio": 32.90,
        "unidad": "kg",
        "descripcion": "La piña contiene bromelina y vitamina C."
    },
    "papaya": {
        "precio": 27.90,
        "unidad": "kg",
        "descripcion": "La papaya favorece la digestión."
    },
    "mango": {
        "precio": 45.90,
        "unidad": "kg",
        "descripcion": "El mango contiene vitaminas A y C."
    },
    "melon": {
        "precio": 25.90,
        "unidad": "kg",
        "descripcion": "El melón es hidratante y ligero."
    },
    "guayaba": {
        "precio": 49.90,
        "unidad": "kg",
        "descripcion": "La guayaba es rica en vitamina C."
    }
}


@app.route("/")
def index():
    return render_template("index.html", frutas_info=frutas_info)


@app.route("/predecir", methods=["POST"])
def predecir():
    data = request.json

    if "imagen" not in data:
        return jsonify({"error": "No se recibió imagen"}), 400

    imagen_base64 = data["imagen"].split(",")[1]
    imagen_bytes = base64.b64decode(imagen_base64)

    imagen = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
    imagen = imagen.resize((IMG_SIZE, IMG_SIZE))

    img_array = np.array(imagen)
    img_array = np.expand_dims(img_array, axis=0)

    predicciones = model.predict(img_array)[0]

    top_5_indices = np.argsort(predicciones)[-5:][::-1]

    resultados = []

    for indice in top_5_indices:
        clase = class_names[indice]
        confianza = float(predicciones[indice]) * 100

        info = frutas_info.get(clase, {
            "precio": 0,
            "unidad": "kg",
            "descripcion": "Información no disponible."
        })

        resultados.append({
            "clase": clase,
            "confianza": round(confianza, 2),
            "precio": info["precio"],
            "unidad": info["unidad"],
            "descripcion": info["descripcion"]
        })

    return jsonify({"resultados": resultados})


if __name__ == "__main__":
    app.run(debug=True)