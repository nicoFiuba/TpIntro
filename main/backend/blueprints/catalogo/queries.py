from db import get_connection

def obtener_todos_los_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

def obtener_producto_por_id(producto_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    return producto

def obtener_producto_por_categoria(producto_tipo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE categoria = %s", (producto_tipo,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    return producto

def obtener_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW COLUMNS FROM productos LIKE 'categoria'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    type_str = result['Type']
    valores = type_str.strip("enum()").replace("'", "").split(",")
    return [v.strip() for v in valores]

def crear_producto(datos_producto):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO productos (nombre, descripcion, precio, stock, categoria, imagen, publico_destinado, tipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        datos_producto.get('nombre'),
        datos_producto.get('descripcion'),
        datos_producto.get('precio'),
        datos_producto.get('stock'),
        datos_producto.get('categoria'),
        datos_producto.get('imagen'),
        datos_producto.get('publico_destinado'),
        datos_producto.get('tipo')
    )

    cursor.execute(sql, valores)
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    return nuevo_id

def actualizar_producto(producto_id, datos_producto):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = """
    UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s, categoria = %s, imagen = %s, edad = %s, tipo = %s WHERE id = %s
    """

    valores = (
        datos_producto.get('nombre'),
        datos_producto.get('descripcion'),
        datos_producto.get('precio'),
        datos_producto.get('stock'),
        datos_producto.get('categoria'),
        datos_producto.get('imagen'),
        datos_producto.get('publico_destinado'),
        datos_producto.get('tipo'),
        producto_id
    )
    
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.rowcount > 0

def eliminar_producto(producto_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return cursor.rowcount > 0
