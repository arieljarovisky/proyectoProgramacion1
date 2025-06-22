"""
Define las rutas (endpoints) para operaciones relacionadas con usuarios en la API de Caja Plus.

Términos clave:
- Blueprint: Permite modularizar rutas en Flask, agrupando endpoints relacionados bajo un mismo prefijo.
- Endpoint: URL a la que se puede acceder desde el frontend para realizar una acción (registrar, obtener, actualizar, eliminar, loguear usuarios).
- Controller: Función en el backend que maneja la lógica para cada acción sobre los usuarios.

Este archivo vincula las rutas HTTP con sus controladores respectivos. No contiene lógica de negocio, solo el "enrutamiento".
"""

from flask import Blueprint
from controllers.usuarios_controllers import (
    registrar_usuario,
    obtener_usuarios,
    actualizar_usuario,
    eliminar_usuario,
    login_usuario
)

# Blueprint para usuarios.
# url_prefix='/api/usuarios' hace que todas las rutas definidas aquí comiencen con ese prefijo.
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

# =============================
# Rutas (endpoints) de usuarios
# =============================

# POST /api/usuarios/
# Registrar nuevo usuario (alta)
usuarios_bp.route('/', methods=['POST'])(registrar_usuario)

# GET /api/usuarios/
# Obtener todos los usuarios (listado)
usuarios_bp.route('/', methods=['GET'])(obtener_usuarios)

# PUT /api/usuarios/<usuario_id>
# Actualizar usuario por su ID (modificación de datos)
usuarios_bp.route('/<int:usuario_id>', methods=['PUT'])(actualizar_usuario)

# DELETE /api/usuarios/<usuario_id>
# Eliminar usuario por su ID (baja)
usuarios_bp.route('/<int:usuario_id>', methods=['DELETE'])(eliminar_usuario)

# POST /api/usuarios/login
# Login de usuario (autenticación, inicio de sesión)
usuarios_bp.route('/login', methods=['POST'])(login_usuario)

