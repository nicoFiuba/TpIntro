from flask import Flask, render_template, request
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
    return render_template("index.html", categorias=categorias, productos=productos)

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
    categorias = invocar_categorias()
    return render_template("shopping-cart.html", categorias=categorias)

@app.route('/product-details')
def product_details():
    categorias = invocar_categorias()
    return render_template("product-details.html", categorias=categorias)

@app.route('/my-account')
def my_account():
    perfil_usuario = invocar_perfil_usuario()
    categorias = invocar_categorias()
    return render_template("my-account.html", categorias=categorias, perfil_usuario=perfil_usuario)

@app.route('/purchase-completed')
def purchase_completed():
    categorias = invocar_categorias()
    return render_template("purchase-completed.html", categorias=categorias)

@app.route('/contact-us')
def contact_us():
    categorias = invocar_categorias()
    return render_template("contact-us.html", categorias=categorias)

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)