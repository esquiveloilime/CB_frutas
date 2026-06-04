import os
import shutil

DATASET_BASE = "datasetv3"
FOTOS_REALES = "fotos_reales"
DATASET_NUEVO = "datasetv4"

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

EXTENSIONES = [".jpg", ".jpeg", ".png"]


def copiar_dataset_base():
    if os.path.exists(DATASET_NUEVO):
        shutil.rmtree(DATASET_NUEVO)

    shutil.copytree(DATASET_BASE, DATASET_NUEVO)
    print("Dataset base copiado a datasetv4.")


def agregar_fotos_reales():
    for clase in CLASES:
        carpeta_reales = os.path.join(FOTOS_REALES, clase)
        carpeta_destino = os.path.join(DATASET_NUEVO, "train", clase)

        os.makedirs(carpeta_destino, exist_ok=True)

        if not os.path.exists(carpeta_reales):
            print(f"No hay fotos reales para: {clase}")
            continue

        contador = len([
            archivo for archivo in os.listdir(carpeta_destino)
            if archivo.lower().endswith(tuple(EXTENSIONES))
        ]) + 1

        agregadas = 0

        for archivo in os.listdir(carpeta_reales):
            extension = os.path.splitext(archivo)[1].lower()

            if extension not in EXTENSIONES:
                continue

            ruta_origen = os.path.join(carpeta_reales, archivo)

            nuevo_nombre = f"{clase}_real_{contador}{extension}"
            ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)

            shutil.copy2(ruta_origen, ruta_destino)

            contador += 1
            agregadas += 1

        print(f"{clase}: {agregadas} fotos reales agregadas a train.")


def contar_dataset():
    print("\nConteo final de datasetv4  :")

    for tipo in ["train", "test"]:
        print(f"\n{tipo.upper()}")

        for clase in CLASES:
            carpeta = os.path.join(DATASET_NUEVO, tipo, clase)

            if not os.path.exists(carpeta):
                total = 0
            else:
                total = len([
                    archivo for archivo in os.listdir(carpeta)
                    if archivo.lower().endswith(tuple(EXTENSIONES))
                ])

            print(f"{clase}: {total}")


copiar_dataset_base()
agregar_fotos_reales()
contar_dataset()

print("\nDataset v4 creado correctamente.")