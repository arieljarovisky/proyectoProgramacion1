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
    if not data or 'monto' not in data or 'descripcion' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    nuevo_pago = {
        'id': str(len(cargar_pagos()) +1),
        'fecha': data.get('fecha') or request.headers.get('X-Date') or '2025-05-14',
        'descripcion': data['descripcion'],
        'monto': data['monto']
    }
    
    pagos =cargar_pagos()
    pagos.append(nuevo_pago)
    guardar_pagos(pagos)
    
    return jsonify({'message': 'Pago registrado correctamente'}), 201   

