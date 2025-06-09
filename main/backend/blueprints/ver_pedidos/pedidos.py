from flask import Blueprint, request, jsonify
from db import get_connection

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/')
def get_pedidos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pedidos")
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No hay pedidos"
    return jsonify(pedidos)

@pedidos_bp.route('idpedido/<int:idp>')
def get_idp_pedido(idp):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pedidos WHERE idpedido = %s", (idp,))
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No existe ningun pedido con ID de Pedido {idp}"
    return jsonify(pedidos)

@pedidos_bp.route('fecha/<string:fecha>')
def get_fecha_pedido(fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pedidos WHERE fecha >= %s", (fecha,))
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No existe ningun pedido hecho en {fecha} o despues"
    return jsonify(pedidos)

@pedidos_bp.route('producto/<string:producto>')
def get_producto_pedido(producto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pedidos WHERE  producto = %s", (producto,))
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No hay ningun pedido del producto {producto}"
    return jsonify(pedidos)