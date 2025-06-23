"""
Este archivo define las rutas relacionadas con la gestión de usuarios en la aplicación Flask.
Utiliza un Blueprint llamado 'usuarios_bp' con prefijo '/api/usuarios' para agrupar las rutas 
de registro, consulta, edición, eliminación y login de usuarios.

Cada ruta está conectada a una función del controlador 'usuarios_controllers'.
"""

# Importa Blueprint desde Flask para agrupar rutas bajo un mismo prefijo
from flask import Blueprint

# Importa las funciones del controlador de usuarios
from controllers.usuarios_controllers import (
    registrar_usuario,      # Función para registrar un nuevo usuario
    obtener_usuarios,       # Función para obtener todos los usuarios registrados
    actualizar_usuario,     # Función para actualizar un usuario existente
    eliminar_usuario,       # Función para eliminar un usuario existente
    login_usuario           # Función para autenticar un usuario
)

# Crea el Blueprint 'usuarios_bp' con prefijo de URL '/api/usuarios'
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

# ---------- RUTAS ----------

# Ruta para registrar un nuevo usuario mediante POST
usuarios_bp.route('/', methods=['POST'])(registrar_usuario)

# Ruta para obtener la lista de todos los usuarios mediante GET
usuarios_bp.route('/', methods=['GET'])(obtener_usuarios)

# Ruta para actualizar los datos de un usuario por ID usando PUT
usuarios_bp.route('/<int:usuario_id>', methods=['PUT'])(actualizar_usuario)

# Ruta para eliminar un usuario por ID usando DELETE
usuarios_bp.route('/<int:usuario_id>', methods=['DELETE'])(eliminar_usuario)

# Ruta para hacer login de usuario usando POST
usuarios_bp.route('/login', methods=['POST'])(login_usuario)
