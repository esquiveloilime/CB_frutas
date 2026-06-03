import os
import shutil

TRAIN_ORIGEN = "fruits-360-100x100/Training"
TEST_ORIGEN = "fruits-360-100x100/Test"
DESTINO = "dataset_frutas"

clases = {
    "manzana": [
        "Apple 5", "Apple 6", "Apple 7", "Apple 8", "Apple 9",
        "Apple 10", "Apple 11", "Apple 12", "Apple 13", "Apple 14",
        "Apple 17", "Apple 18", "Apple 19", "Apple 20", "Apple 21",
        "Apple 22", "Apple 23", "Apple Braeburn 1", "Apple Crimson Snow 1",
        "Apple Golden 1", "Apple Golden 2", "Apple Golden 3",
        "Apple Granny Smith 1", "Apple Pink Lady 1", "Apple Red 1",
        "Apple Red 2", "Apple Red 3", "Apple Red Delicious 1",
        "Apple Red Yellow 1", "Apple Red Yellow 2"
    ],
    "platano": [
        "Banana 1", "Banana 3", "Banana 4",
        "Banana Lady Finger 1", "Banana Red 1"
    ],
    "naranja": [
        "Orange 1", "Orange 2", "Orange 3", "orange 4", "Orange peeled 1"
    ],
    "limon": [
        "Lemon 1", "Lemon Meyer 1", "Limes 1"
    ],
    "pepino": [
        "Cucumber 1", "Cucumber 3", "Cucumber 4", "Cucumber 5",
        "Cucumber 6", "Cucumber 7", "Cucumber 8", "Cucumber 9",
        "Cucumber 10", "Cucumber 11", "Cucumber 12", "Cucumber 13",
        "Pepino 1"
    ],
    "durazno": [
        "Peach 1", "Peach 2", "Peach 3", "Peach 4",
        "Peach 5", "Peach 6", "Peach Flat 1"
    ],
    "kiwi": ["Kiwi 1"],
    "sandia": ["Watermelon 1"],
    "pina": ["Pineapple 1", "Pineapple Mini 1"],
    "papaya": ["Papaya 1", "Papaya 2"],
    "mango": ["Mango 1", "Mango Red 1"],
    "melon": [
        "Melon Piel de Sapo 1",
        "Cantaloupe 1",
        "Cantaloupe 2",
        "Cantaloupe 3"
    ],
    "guayaba": ["Guava 1"]
}


def copiar_dataset(origen, destino_tipo):
    print(f"\nCopiando desde: {origen}")
    print(f"Hacia: {destino_tipo}\n")

    os.makedirs(destino_tipo, exist_ok=True)

    for clase_final, carpetas_origen in clases.items():
        carpeta_destino = os.path.join(destino_tipo, clase_final)
        os.makedirs(carpeta_destino, exist_ok=True)

        contador = 1

        for carpeta in carpetas_origen:
            ruta_origen = os.path.join(origen, carpeta)

            if not os.path.exists(ruta_origen):
                print(f"No encontrada: {ruta_origen}")
                continue

            for archivo in os.listdir(ruta_origen):
                ruta_archivo = os.path.join(ruta_origen, archivo)

                if os.path.isfile(ruta_archivo):
                    extension = os.path.splitext(archivo)[1]
                    nuevo_nombre = f"{clase_final}_{contador}{extension}"
                    ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)

                    shutil.copy2(ruta_archivo, ruta_destino)
                    contador += 1

        print(f"Clase {clase_final}: {contador - 1} imágenes copiadas")


if os.path.exists(DESTINO):
    shutil.rmtree(DESTINO)

copiar_dataset(TRAIN_ORIGEN, os.path.join(DESTINO, "train"))
copiar_dataset(TEST_ORIGEN, os.path.join(DESTINO, "test"))

print("\nDataset preparado correctamente.")