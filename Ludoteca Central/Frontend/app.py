from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/shop-mixed')
def shop_mixed():
    return render_template("shop-mixed.html")

@app.route('/wishlist')
def wishlist():
    return render_template("wishlist.html")

@app.route('/shopping-cart')
def shopping_cart():
    return render_template("shopping-cart.html")

@app.route('/product-details')
def product_details():
    return render_template("product-details.html")

@app.route('/checkout')
def checkout():
    return render_template("checkout.html")

@app.route('/my-account')
def my_account():
    return render_template("my-account.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/sign-up')
def sign_up():
    return render_template("sign-up.html")

@app.route('/forgot-password')
def forgot_password():
    return render_template("forgot-password.html")

@app.route('/error404')
def error404():
    return render_template("error404.html")

@app.route('/purchase-completed')
def purchase_completed():
    return render_template("purchase-completed.html")

@app.route('/purchase-failed')
def purchase_failed():
    return render_template("purchase-failed.html")

@app.route('/message-sent')
def message_sent():
    return render_template("message-sent.html")

@app.route('/verification')
def verification():
    return render_template("verification.html")

@app.route('/contact-us')
def contact_us():
    return render_template("contact-us.html")

@app.route('/about-us')
def about_us():
    return render_template("about-us.html")

if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)