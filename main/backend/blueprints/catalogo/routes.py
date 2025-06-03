from flask import request, jsonify
from . import productos_bp
from . queries import (
    obtener_todos_los_productos,
    obtener_producto_por_id,
    crear_producto,
    actualizar_producto,
    eliminar_producto
)

@productos_bp.route('/api/productos', methods=['GET'])
def listar_productos():
    productos = obtener_todos_los_productos()
    return jsonify(productos), 200

@productos_bp.route('/api/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(id):
    producto = obtener_producto_por_id(id)
    if producto:
        return jsonify(producto), 200
    return jsonify({'error': 'Producto no encontrado'}), 404

@productos_bp.route('/api/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()
    nuevo_id = crear_producto(datos)
    return jsonify({'mensaje'; 'Producto creado', 'id': nuevo_id}), 201

@productos_bp.route('/api/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.get_json()
    exito = actualizar_producto(id, data)
    if exito:
        return jsonify({'mensaje': 'Producto actualizado'}), 200
    return jsonify({'error': 'Producto no encontrado'}), 404

@productos_bp.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar(id):
    exito = eliminar_producto(id)
    if exito:
        return jsonify({'mensaje': 'Producto eliminado'}), 200
    return jsonify({'error': 'Producto no encontrado'}), 404

