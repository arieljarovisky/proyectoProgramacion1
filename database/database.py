import os

DATABASE_FILE = "caja_data.txt"

def inicializar_archivo():
    """Crea el archivo de base de datos si no existe."""
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w") as f:
            f.write("")  # Archivo vacío para iniciar
