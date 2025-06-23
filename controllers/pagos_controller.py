"""
Este archivo gestiona el registro y la obtención de pagos dentro del sistema Flask de Caja Plus.

Incluye:
- Manejo del archivo JSON `pagos.json` donde se almacenan los pagos realizados.
- Endpoints para obtener todos los pagos (`GET`) y registrar un nuevo pago (`POST`).
- Validaciones de datos ingresados: campos requeridos, monto válido y formatos de fecha.
- Conversión de pagos en egresos registrados dentro de `caja.json`, actualizando el saldo y movimientos.

Formatos de fecha aceptados al registrar un pago:
- ISO: YYYY-MM-DD
- Europeo: DD/MM/YYYY
- Americano: MM/DD/YYYY
"""
import json  # Módulo estándar para manejar archivos JSON (leer y escribir).
from flask import request, jsonify  # request se usa para acceder a datos del body de la petición HTTP, jsonify para enviar respuestas JSON.
from pathlib import Path  # Permite trabajar con rutas de archivos de forma segura y multiplataforma.
from datetime import datetime  # Para trabajar con fechas y horas.
from controllers.caja_controller import cargar_caja, guardar_caja  # Funciones para cargar y guardar el estado de la caja desde otro módulo.

PAGOS_PATH = Path("./data/pagos.json")  # Define la ruta al archivo donde se almacenan los pagos.

def cargar_pagos():
    """
    Carga la lista de pagos desde el archivo `pagos.json`.
    Si el archivo no existe, lo crea vacío y devuelve una lista vacía.
    """
    if not PAGOS_PATH.exists():  # Verifica si el archivo no existe.
        PAGOS_PATH.parent.mkdir(parents=True, exist_ok=True)  # Crea la carpeta `data/` si no existe.
        with open(PAGOS_PATH, "w", encoding="utf-8") as f:  # Crea el archivo vacío.
            json.dump([], f)  # Escribe una lista vacía en el archivo.
        return []  # Retorna una lista vacía.

    with open(PAGOS_PATH, "r", encoding="utf-8") as f:  # Abre el archivo existente.
        return json.load(f)  # Devuelve el contenido como lista de pagos.

def guardar_pagos(pagos):
    """
    Guarda la lista de pagos en el archivo `pagos.json` con formato legible.
    """
    with open(PAGOS_PATH, "w", encoding="utf-8") as f:  # Abre el archivo en modo escritura.
        json.dump(pagos, f, indent=2, ensure_ascii=False)  # Guarda los pagos con indentación y soporte UTF-8.

def obtener_pagos():
    """
    Endpoint GET que devuelve todos los pagos registrados en formato JSON.
    """
    pagos = cargar_pagos()  # Carga todos los pagos.
    return jsonify(pagos), 200  # Retorna la lista con código HTTP 200 (OK).

def registrar_pago():
    """
    Endpoint POST que registra un nuevo pago, validando los datos y actualizando la caja.

    Incluye:
    - Validación de campos obligatorios y del monto.
    - Interpretación de fechas en distintos formatos.
    - Registro del pago en `pagos.json`.
    - Registro del egreso equivalente en `caja.json`.
    """
    data = request.get_json()  # Obtiene los datos enviados en el cuerpo del request (formato JSON).
    campos_requeridos = ["destinatario", "concepto", "descripcion", "monto", "metodo"]  # Lista de claves obligatorias.

    # Validación: todos los campos requeridos deben estar presentes y no vacíos.
    if not data or not all(campo in data and data[campo] for campo in campos_requeridos):
        return jsonify({"error": "Faltan campos requeridos"}), 400  # Error HTTP 400 si falta alguno.

    # Validación del campo monto: debe ser un número positivo.
    try:
        monto = float(data["monto"])  # Intenta convertir el valor a float.
        if monto <= 0:
            return jsonify({"error": "El monto debe ser mayor a cero"}), 400
    except Exception:
        return jsonify({"error": "El monto no es válido"}), 400  # Error si no se puede convertir a número.

    # Si se especifica fecha, intentar interpretarla. Si no, usar la fecha actual.
    fecha_input = data.get("fecha")
    if fecha_input:
        fecha_str = fecha_input.strip()
        dt = None
        try:
            dt = datetime.fromisoformat(fecha_str)  # Intenta formato ISO (YYYY-MM-DD).
        except ValueError:
            try:
                dt_date = datetime.strptime(fecha_str, "%d/%m/%Y")  # Intenta DD/MM/YYYY.
                now = datetime.now()
                dt = dt_date.replace(hour=now.hour, minute=now.minute, second=now.second)
            except ValueError:
                try:
                    dt_date = datetime.strptime(fecha_str, "%m/%d/%Y")  # Intenta MM/DD/YYYY.
                    now = datetime.now()
                    dt = dt_date.replace(hour=now.hour, minute=now.minute, second=now.second)
                except ValueError:
                    return jsonify({
                        "error": "Formato de fecha inválido. Acepto YYYY-MM-DD, DD/MM/YYYY o MM/DD/YYYY"
                    }), 400
        fecha_pago = dt.strftime("%Y-%m-%d %H:%M:%S")  # Convierte a string final.
    else:
        fecha_pago = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Si no hay fecha, usa la actual.

    # Agrega el nuevo pago a la lista de pagos
    pagos = cargar_pagos()
    nuevo_pago = {
        "id": str(len(pagos) + 1),  # Genera ID secuencial como string.
        "fecha": fecha_pago,
        "destinatario": data["destinatario"],
        "concepto": data["concepto"],
        "descripcion": data["descripcion"],
        "monto": monto,
        "metodo": data["metodo"],
    }
    pagos.append(nuevo_pago)
    guardar_pagos(pagos)  # Guarda la lista actualizada.

    # Carga la caja actual y registra el egreso correspondiente.
    caja = cargar_caja()
    egreso = {
        "id": nuevo_pago["id"],
        "tipo": "egreso",  # Define el tipo de movimiento.
        "monto": monto,
        "descripcion": data["descripcion"],
        "fecha": fecha_pago,
        "detalles": {
            "destinatario": data["destinatario"],
            "concepto": data["concepto"],
            "metodo": data["metodo"],
        },
    }
    caja["saldo"] -= monto  # Resta el monto al saldo actual de caja.
    caja["movimientos"].append(egreso)  # Agrega el movimiento como egreso.
    guardar_caja(caja)  # Guarda la caja actualizada.

    return jsonify({"message": "Pago y egreso registrados correctamente"}), 201  # Respuesta de éxito.
