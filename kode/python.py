from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.debug = True

app.config['MYSQL_HOST'] = '10.2.4.76'
app.config['MYSQL_USER'] = 'adriatik'
app.config['MYSQL_PASSWORD'] = 'Adriatik.123'
app.config['MYSQL_DB'] = 'restauran'

mysql = MySQL(app)


app.route('/reservasjoner', methods=['GET'])
def display():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM contact_info")
    data = cursor.fetchall()
    return render_template('reservasjoner.html', info_table=data)


app.run(host='localhost', port=5000)