from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Nødvendig for session-håndtering
app.config['MYSQL_HOST'] = 'localhost'  # MySQL-server adresse
app.config['MYSQL_USER'] = 'root'      # Brukernavn for MySQL
app.config['MYSQL_PASSWORD'] = 'password'  # Passord for MySQL
app.config['MYSQL_DB'] = 'webshop'    # Navn på databasen

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    product_list = cur.fetchall()
    cur.close()
    return render_template('products.html', products=product_list)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append({'product_id': product_id, 'quantity': quantity})
        session.modified = True
        
        return redirect(url_for('cart'))
    
    cart_items = []
    if 'cart' in session:
        cur = mysql.connection.cursor()
        for item in session['cart']:
            cur.execute("SELECT id, name, price FROM products WHERE id = %s", (item['product_id'],))
            product = cur.fetchone()
            if product:
                cart_items.append((product[0], product[1], item['quantity'], product[2] * item['quantity']))
        cur.close()

    return render_template('cart.html', cart=cart_items)

@app.route('/checkout', methods=['POST'])
def checkout():
    session.pop('cart', None)  # Tøm handlekurven
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
