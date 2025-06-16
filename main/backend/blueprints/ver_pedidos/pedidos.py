from flask import Blueprint, request, jsonify, render_template
from db import get_connection
import pymysql

pedidos_bp = Blueprint('pedidos', __name__)

# Nueva ruta para la página de confirmación
@pedidos_bp.route('/completado/<int:pedido_id>')
def compra_completada(pedido_id):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # Obtener info básica del pedido
            cursor.execute("""
                SELECT p.id, p.fecha, u.username as cliente,
                SUM(pd.cantidad * pd.precio) as total
                FROM Pedido p
                JOIN Usuario u ON p.usuario_id = u.id
                JOIN PedidoDetalle pd ON p.id = pd.pedido_id
                WHERE p.id = %s
                GROUP BY p.id
            """, (pedido_id,))
            pedido = cursor.fetchone()

            if not pedido:
                return "Pedido no encontrado", 404

            # Obtener productos del pedido
            cursor.execute("""
                SELECT pr.nombre, pd.cantidad, pd.precio
                FROM PedidoDetalle pd
                JOIN Productos pr ON pd.producto_id = pr.id
                WHERE pd.pedido_id = %s
            """, (pedido_id,))
            pedido['productos'] = cursor.fetchall()

        return render_template('purchase-completed.html', pedido=pedido)
    finally:
        conn.close()

@pedidos_bp.route('/')
def get_pedidos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PedidoDetalle")
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
    cursor.execute("SELECT * FROM PedidoDetalle WHERE pedido_id = %s", (idp,))
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No existe ningun pedido con ID de Pedido {idp}"
    return jsonify(pedidos)


@pedidos_bp.route('producto/<int:idproducto>')
def get_producto_pedido(idproducto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PedidoDetalle WHERE  producto_id = %s", (idproducto,))
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    if not pedidos:
        return f"No hay ningun pedido del producto {idproducto}"
    return jsonify(pedidos)