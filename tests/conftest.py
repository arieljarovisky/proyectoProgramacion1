"""
Este archivo ajusta el path de Python para que los tests puedan importar módulos
del directorio raíz del proyecto (donde reside app.py).
Al insertar la carpeta padre en sys.path, permitimos usar `from app import app`
en tus tests sin complicaciones de rutas.
"""

import sys
import os

# Calcula la ruta al directorio padre (donde está app.py)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Inserta ROOT al inicio de sys.path si no está ya presente
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
