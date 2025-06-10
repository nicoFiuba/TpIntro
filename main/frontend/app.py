from flask import Flask, render_template, request, jsonify
import requests

from urllib.parse import quote
from flask import session

app = Flask(__name__)

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
        resp = requests.get('http://localhost:5000/usuarios/user/5',)
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
    categorias = invocar_categorias()
    carrito = invocar_carrito()
    return render_template("shopping-cart.html", categorias=categorias, perfil_usuario=perfil_usuario, carrito=carrito)

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
    return render_template("my-account.html", categorias=categorias, perfil_usuario=perfil_usuario)

@app.route('/purchase-completed')
def purchase_completed():
    categorias = invocar_categorias()
    perfil_usuario = invocar_perfil_usuario()
    return render_template("purchase-completed.html", categorias=categorias, perfil_usuario=perfil_usuario)

@app.route('/contact-us')
def contact_us():
    perfil_usuario = invocar_perfil_usuario()
    categorias = invocar_categorias()
    return render_template("contact-us.html", categorias=categorias, perfil_usuario=perfil_usuario)

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

    

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)