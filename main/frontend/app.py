from flask import Flask, render_template, request, redirect, url_for, flash
import requests

from urllib.parse import quote
from flask import session

app = Flask(__name__)
app.secret_key = 'clave'

def invocar_categorias():
    try:
        resp = requests.get('http://localhost:5000/catalogo/api/productos/categorias')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar el servicio de categorías: {e}")
        return []

def invocar_productos():
    try:
        resp = requests.get('http://localhost:5000/catalogo/api/productos')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar el servicio de productos: {e}")
        return []

def invocar_productos_por_id(product_id):
    try:
        resp = requests.get(f'http://localhost:5000/catalogo/api/productos/{product_id}')
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                return data[0] if data else None
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar el servicio de productos: {e}")
        return None

def invocar_perfil_usuario():
    try:
        resp = requests.get('http://localhost:5000/usuarios/user/',)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar el servicio de perfil de usuario: {e}")
        return {}

def invocar_pedidos():
    try:
        resp = requests.get('http://localhost:5000/pedidos')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar pedidos {e}")
        return []
    
def invocar_pedidos_por_id(id):
    try:
        resp = requests.get(f'http://localhost:5000/pedidos/idpedido/{id}')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar pedidos {e}")
        return []

def invocar_carrito():
    try:
        resp = requests.get('http://localhost:5000/cart')
        if resp.status_code == 200:
            return resp.json()
        else:
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error al invocar el carrito: {e}")
        return {}

def invocar_busqueda_productos(consulta):
    try:
        resp = requests.get(f'http://localhost:5000/catalogo/buscar?q={consulta}')
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error al buscar productos: {e}")
        return []

@app.context_processor
def inject_cart_count():
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    return dict(cart_count=cart_count)

@app.context_processor
def poner_nombre():
    return dict(BRAND_NAME="Ludoteca central")

@app.context_processor
def poner_mail():
    return dict(MAIL= "ludotecacentral@gmail.com")

@app.context_processor
def poner_mail():
    return dict(NUMERO= "+54 11 60217938")

@app.route('/')
def index():
    productos = invocar_productos()
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    return render_template("index.html", categorias=categorias, productos=productos, perfil_usuario=perfil_usuario)

@app.route('/shop-mixed')
def shop_mixed():
    categoria = request.args.get('categoria')
    perfil_usuario = invocar_perfil_usuario()
    productos = invocar_productos()
    categorias = invocar_categorias()
    if not categoria:  
        categoria = None
    if categoria:
        productos = [p for p in productos if p.get('categoria') == categoria]
    return render_template(
        "shop-mixed.html",
        categorias=categorias,
        productos=productos,
        perfil_usuario=perfil_usuario,
        categoria=categoria
    )

@app.route('/shopping-cart')
def shopping_cart():
    perfil_usuario = invocar_perfil_usuario()
    productos = invocar_productos()
    categorias = invocar_categorias()
    carrito = invocar_carrito()
    return render_template("shopping-cart.html", categorias=categorias, perfil_usuario=perfil_usuario, carrito=carrito, productos=productos)

@app.route('/product-details/<int:product_id>')
def product_details(product_id):
    perfil_usuario = invocar_perfil_usuario()
    categorias = invocar_categorias()
    producto = invocar_productos_por_id(product_id)
    return render_template(
        "product-details.html",
        categorias=categorias,
        perfil_usuario=perfil_usuario,
        product=producto
    )

@app.route('/my-account')
def my_account():
    perfil_usuario = invocar_perfil_usuario()
    categorias = invocar_categorias()
    productos = invocar_productos()
    return render_template("my-account.html", categorias=categorias, perfil_usuario=perfil_usuario, productos=productos)

@app.route('/purchase-completed')
def purchase_completed():
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    productos = invocar_productos()
    return render_template("purchase-completed.html", categorias=categorias, perfil_usuario=perfil_usuario, productos=productos)

@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    perfil_usuario = invocar_perfil_usuario()
    categorias = invocar_categorias()
    productos = invocar_productos()
    if request.method == 'POST':
        flash("Gracias por compartir tu opinion", "success")
    return render_template("contact-us.html", categorias=categorias, perfil_usuario=perfil_usuario, productos=productos)

@app.route('/administrar-pagina')
def administrar_pagina():
    verpedidos = invocar_pedidos()
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    productos = invocar_productos()
    
    return render_template("administrar-pagina.html", verpedidos=verpedidos, perfil_usuario=perfil_usuario, categorias=categorias, productos=productos)

@app.route('/administrar-pagina/pedidos', methods=['GET','POST'])
def administrar_pedidos():
    verpedidos = invocar_pedidos()
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    productos = invocar_productos()
    if request.method == 'POST':
        id = request.form['id_pedido']
        verpedidosid = invocar_pedidos_por_id(id)
        return render_template('pedidos.html', datos=verpedidosid, perfil_usuario=perfil_usuario, categorias=categorias, productos=productos)
    else:
        return render_template('pedidos.html', datos=verpedidos, perfil_usuario=perfil_usuario, categorias=categorias, productos=productos)

@app.route('/buscar')
def buscar_productos():
    consulta = request.args.get('q', '')
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    productos = []
    if consulta:
        productos = invocar_busqueda_productos(consulta)
    return render_template(
        "resultados_busqueda.html",
        categorias=categorias,
        productos=productos,
        perfil_usuario=perfil_usuario,
        consulta=consulta
    )

@app.route('/eliminar-producto/<int:product_id>', methods=['POST'])
def eliminar_producto(product_id):
    try:
        resp = requests.delete(f'http://localhost:5000/catalogo/api/productos/{product_id}')
        if resp.status_code == 200:
            flash('Producto eliminado exitosamente', 'success')
        else:
            flash('No se pudo eliminar el producto', 'danger')
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar el producto: {e}")
        flash('Error al eliminar el producto', 'danger')
    return redirect(url_for('administrar_pagina'))


@app.route('/agregar-producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria = request.form['categoria']
        stock = request.form.get('stock')
        if not nombre or not descripcion or not precio or not categoria:
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('administrar_pagina'))

        try:
            data = {
                'nombre': nombre,
                'descripcion': descripcion,
                'precio': precio,
                'stock': stock,
                'categoria': categoria
                
            }
            resp = requests.post('http://localhost:5000/catalogo/api/productos', json=data)
            if resp.status_code == 201:
                flash('Producto agregado exitosamente', 'success')
            else:
                flash('No se pudo agregar el producto', 'danger')
        except requests.exceptions.RequestException as e:
            print(f"Error al agregar el producto: {e}")
            flash('Error al agregar el producto', 'danger')
        print(resp.status_code, resp.text)
    return redirect(url_for('shop_mixed'))
    
@app.route('/ingresar', methods=['POST'])
def ingresar():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        data = {
            'username': username,
            'password': password
        }

        resp = requests.post('http://localhost:5000/usuarios/auth/login', data=data)

        if resp.status_code == 200:
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('my_account'))
        else:
            flash('Error al iniciar sesión: ' + resp.json().get('message', 'Error'), 'danger')      
            return redirect(url_for('index'))
    except requests.exceptions.RequestException as e:
        flash('No se pudo conectar al servicio de autenticación', 'danger')
        return redirect(url_for('index'))

@app.route('/registro', methods=['POST'])
def registro():    
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    data = {
            "username": username,
            "password": password,
            "email": email
        }
    
    resp = requests.post('http://localhost:5000/usuarios/auth/register', json=data)

    if resp.status_code == 201:
        flash('Registro exitoso')
        return redirect(url_for('index'))
    else:
        flash('Error al registrar: ' + resp.json().get('message', ''))
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)