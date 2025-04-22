from flask import Blueprint
from controllers.usuarios_controllers import (
    registrar_usuario,
    obtener_usuarios,
    actualizar_usuario,
    eliminar_usuario,
    login_usuario
)

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

# Registrar nuevo usuario
usuarios_bp.route('/', methods=['POST'])(registrar_usuario)

# Obtener todos los usuarios
usuarios_bp.route('/', methods=['GET'])(obtener_usuarios)

# Actualizar usuario por ID
usuarios_bp.route('/<int:usuario_id>', methods=['PUT'])(actualizar_usuario)

# Eliminar usuario por ID
usuarios_bp.route('/<int:usuario_id>', methods=['DELETE'])(eliminar_usuario)

# Login de usuario
usuarios_bp.route('/login', methods=['POST'])(login_usuario)
