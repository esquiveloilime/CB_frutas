import tensorflow as tf
import numpy as np

IMG_SIZE = 100

MODEL_PATH = "modelo/mejor_modelo.keras"
CLASSES_PATH = "modelo/clases.txt"
IMAGE_PATH = "prueba.jpg"

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

img = tf.keras.utils.load_img(
    IMAGE_PATH,
    target_size=(IMG_SIZE, IMG_SIZE)
)

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

predictions = model.predict(img_array)
score = predictions[0]

indice = np.argmax(score)
clase = class_names[indice]
confianza = 100 * np.max(score)

print(f"Fruta detectada: {clase}")
print(f"Confianza: {confianza:.2f}%")

print("\nTop 3 predicciones:")
top_3 = np.argsort(score)[-3:][::-1]

for i in top_3:
    print(f"{class_names[i]}: {100 * score[i]:.2f}%")