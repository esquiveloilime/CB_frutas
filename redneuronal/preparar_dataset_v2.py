import os
import random
import shutil

# Dataset original está una carpeta arriba de redneuronal
TRAIN_ORIGEN = "../fruits-360-100x100/Training"
TEST_ORIGEN = "../fruits-360-100x100/Test"

# Nuevo dataset filtrado
DESTINO = "datasetv2"

# Cantidad máxima para balancear clases
MAX_TRAIN_POR_CLASE = 500
MAX_TEST_POR_CLASE = 150

SEED = 123
random.seed(SEED)

clases = {
    "limon": [
        "Lemon 1",
        "Lemon Meyer 1",
        "Limes 1"
    ],
    "mango": [
        "Mango 1",
        "Mango Red 1"
    ],
    "manzana": [
        "Apple 5"
    ],
    "melon": [
        "Melon Piel de Sapo 1",
        "Cantaloupe 1",
        "Cantaloupe 2",
        "Cantaloupe 3"
    ],
    "naranja": [
        "Orange 1",
        "Orange 2",
        "Orange 3",
        "orange 4",
        "Orange peeled 1"
    ],
    "pepino": [
        "Cucumber 1",
        "Cucumber 3",
        "Cucumber 4",
        "Cucumber 5",
        "Cucumber 6",
        "Cucumber 7",
        "Cucumber 8",
        "Cucumber 9",
        "Cucumber 10",
        "Cucumber 11",
        "Cucumber 12",
        "Cucumber 13",
        "Pepino 1"
    ],
    "pina": [
        "Pineapple 1",
        "Pineapple Mini 1"
    ],
    "platano": [
        "Banana 1",
        "Banana 3",
        "Banana 4",
        "Banana Lady Finger 1",
        "Banana Red 1"
    ],
    "sandia": [
        "Watermelon 1"
    ]
}


def obtener_imagenes(origen, carpetas):
    imagenes = []

    for carpeta in carpetas:
        ruta_carpeta = os.path.join(origen, carpeta)

        if not os.path.exists(ruta_carpeta):
            print(f"No encontrada: {ruta_carpeta}")
            continue

        for archivo in os.listdir(ruta_carpeta):
            ruta_archivo = os.path.join(ruta_carpeta, archivo)

            if os.path.isfile(ruta_archivo):
                extension = os.path.splitext(archivo)[1].lower()

                if extension in [".jpg", ".jpeg", ".png"]:
                    imagenes.append(ruta_archivo)

    return imagenes


def copiar_clase(origen, destino_tipo, clase_final, carpetas_origen, max_imagenes):
    imagenes = obtener_imagenes(origen, carpetas_origen)

    random.shuffle(imagenes)

    if len(imagenes) > max_imagenes:
        imagenes = imagenes[:max_imagenes]

    carpeta_destino = os.path.join(destino_tipo, clase_final)
    os.makedirs(carpeta_destino, exist_ok=True)

    for i, ruta_origen in enumerate(imagenes, start=1):
        extension = os.path.splitext(ruta_origen)[1].lower()
        nuevo_nombre = f"{clase_final}_{i}{extension}"
        ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)

        shutil.copy2(ruta_origen, ruta_destino)

    print(f"Clase {clase_final}: {len(imagenes)} imágenes copiadas")


def preparar_dataset(origen, destino_tipo, max_por_clase):
    print(f"\nCopiando desde: {origen}")
    print(f"Hacia: {destino_tipo}\n")

    os.makedirs(destino_tipo, exist_ok=True)

    for clase_final, carpetas_origen in clases.items():
        copiar_clase(
            origen=origen,
            destino_tipo=destino_tipo,
            clase_final=clase_final,
            carpetas_origen=carpetas_origen,
            max_imagenes=max_por_clase
        )


if os.path.exists(DESTINO):
    shutil.rmtree(DESTINO)

preparar_dataset(
    TRAIN_ORIGEN,
    os.path.join(DESTINO, "train"),
    MAX_TRAIN_POR_CLASE
)

preparar_dataset(
    TEST_ORIGEN,
    os.path.join(DESTINO, "test"),
    MAX_TEST_POR_CLASE
)

print("\nDataset v2 preparado correctamente.")
print("Estructura:")
print("datasetv2/")
print("├── train/")
print("└── test/")