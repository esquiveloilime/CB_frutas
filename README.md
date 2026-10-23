# Reconocimiento de Frutas mediante CNN

Proyecto de Cómputo Bioinspirado desarrollado con Python, TensorFlow, Keras y Flask.

El sistema permite reconocer frutas mediante una cámara web, utilizando una red neuronal convolucional entrenada para clasificar nueve categorías.

## Requisitos

- Python 3.11
- Cámara web
- Git
- Navegador web

## Instalación

**1. Clonar el repositorio**

```bash
git clone URL_DEL_REPOSITORIO
cd ProyectoFrutasCNN
```

**2. Crear el entorno virtual**

```bash
py -3.11 -m venv .venv
```

**3. Activar el entorno virtual en Git Bash**

```bash
source .venv/Scripts/activate
```

**4. Instalar dependencias**

```bash
python -m pip install -r requirements.txt
```

**5. Ejecutar la aplicación**

```bash
cd PaginaWebCB
../.venv/Scripts/python.exe app.py
```

**6. Abrir el navegador**

Acceder a:

http://127.0.0.1:5000

Permitir el acceso a la cámara, colocar una fruta frente a ella y presionar el botón de análisis.

## Modelo utilizado

El sistema utiliza el modelo V4, entrenado con el dataset Fruit-360 complementado con fotografías reales.

Clases reconocidas:

- Limón
- Mango
- Manzana
- Melón
- Naranja
- Pepino
- Piña
- Plátano
- Sandía

El archivo del modelo debe encontrarse en:

`redneuronal/modelo4/mejor_modelo.keras`

Y las clases en:

`redneuronal/modelo4/clases.txt`
