import json
from flask import request, jsonify
from pathlib import Path

PAGOS_PATH = Path('./data/pagos.json')

def cargar_pagos():
    if not PAGOS_PATH.exists():
        PAGOS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(PAGOS_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []
    
    with open(PAGOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_pagos(pagos):
    with open(PAGOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(pagos, f, indent=2, ensure_ascii=False)

def obtener_pagos():
    pagos =  cargar_pagos()
    return jsonify(pagos), 200

def registrar_pago():
    data = request.get_json()
    campos_requeridos = ['destinatario', 'concepto', 'descripcion', 'monto', 'metodo']

    # Validar todos los campos requeridos
    if not data or not all(campo in data and data[campo] for campo in campos_requeridos):
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    # Validar que monto sea un número positivo
    try:
        monto = float(data['monto'])
        if monto <= 0:
            return jsonify({'error': 'El monto debe ser mayor a cero'}), 400
    except Exception:
        return jsonify({'error': 'El monto no es válido'}), 400

    pagos = cargar_pagos()
    nuevo_pago = {
        'id': str(len(pagos) + 1),
        'fecha': data.get('fecha') or request.headers.get('X-Date') or datetime.now().isoformat(),
        'destinatario': data['destinatario'],
        'concepto': data['concepto'],
        'descripcion': data['descripcion'],
        'monto': monto,
        'metodo': data['metodo']
    }

    pagos.append(nuevo_pago)
    guardar_pagos(pagos)

    return jsonify({'message': 'Pago registrado correctamente'}), 201

