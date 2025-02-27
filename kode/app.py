from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import mysql.connector

# Initialiserer Flask-applikasjonen
app = Flask(__name__)

# Funksjon for å opprette en tilkobling til MySQL-databasen
def get_db_connection():
    return mysql.connector.connect(
        user="adriatik",  # Databasebrukernavn
        password="Adriatik.123",  # Databasepassord (unngå å hardkode passord i produksjon)
        database="restaurant",  # Navnet på databasen
        host="10.2.4.76",  # Vertsmaskinens IP-adresse
        port=3306  # Porten som MySQL bruker
    )

# Rute for hjem-siden
@app.route('/')
def index():
    return render_template('index.html')  # Renderer index.html når brukeren går til '/'

# Rute for meny-siden
@app.route('/menu')
def menu():
    return render_template('menu.html')  # Renderer menu.html for å vise restauranten meny

# Rute for kontaktskjema (GET og POST)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':  # Hvis skjemaet er sendt inn
        # Henter verdier fra skjemaet
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        try:
            # Åpner en tilkobling til databasen
            conn = get_db_connection()
            cursor = conn.cursor()

            # Setter inn dataene i databasen
            cursor.execute("""
                INSERT INTO contact_info (name, email, phone, message)
                VALUES (%s, %s, %s, %s)
            """, (name, email, phone, message))

            conn.commit()  # Bekrefter endringen i databasen
            cursor.close()  # Lukker databasekursoren
            conn.close()  # Lukker databasen

            return "Takk for at du reserverte bord!"  # Bekreftelsesmelding til bruker
        except Exception as e:
            # Hvis en feil oppstår, vis feilmelding
            print(f"Error: {e}")
            return "Error in sending message. Please try again.", 500

    return render_template('contact.html')  # Hvis det er en GET-forespørsel, vis kontaktskjemaet

# Rute for reservasjonssiden (GET og POST)
@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        try:
            # Henter data fra skjemaet
            name = request.form['name']
            phone = request.form['phone']
            people = int(request.form['people'])
            date = request.form['date']
            time = request.form['time']

            # Validerer dato og tid for reservasjonen
            reservation_date = datetime.strptime(date, "%Y-%m-%d").date()
            today = datetime.today().date()
            max_date = today + timedelta(days=30)

            if reservation_date < today or reservation_date > max_date:
                return "Datoen må være innenfor 30 dager fra i dag.", 400  # Feilmelding hvis datoen er utenfor gyldig interval

            # Åpner en tilkobling til databasen
            conn = get_db_connection()
            cursor = conn.cursor()

            # Setter inn reservasjonen i databasen
            cursor.execute("""
                INSERT INTO reservations (name, phone, people, date, time)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, phone, people, date, time))

            conn.commit()  # Bekreft endringene i databasen
            cursor.close()  # Lukker kursoren
            conn.close()  # Lukker tilkoblingen

            return redirect(url_for('reservation_list'))  # Etter vellykket innsending, omdiriger til reservasjon-liste
        except Exception as e:
            print(f"Error: {e}")
            return "Error in processing reservation. Please try again.", 500  # Feil ved innsending av reservasjon

    return render_template('reservation.html')  # Hvis GET, vis skjema for reservasjon

# Rute for takeaway-siden
@app.route('/takeaway')
def takeaway():
    return render_template('takeaway.html')  # Renderer takeaway-siden hvor brukeren kan bestille takeaway

# Rute for å håndtere takeaway-bestillinger via POST
@app.route('/takeaway_orders', methods=['POST'])
def add_takeaway_order():
    data = request.json  # Henter JSON-data fra forespørselen
    try:
        # Koble til databasen
        conn = get_db_connection()
        cursor = conn.cursor()

        # Skriv ut dataene som mottas for debugging
        print(f"Received order: {data}")

        # Setter inn takeaway-bestillingen i databasen
        cursor.execute("""
            INSERT INTO takeaway_orders (name, dish)
            VALUES (%s, %s)
        """, (data['name'], data['dish']))

        conn.commit()  # Bekrefter endringen i databasen
        cursor.close()  # Lukker kursoren
        conn.close()  # Lukker databasen

        # Skriv ut suksessmelding for debugging
        print("Order successfully added to the database.")

        return jsonify({'success': True})  # Returnerer JSON-respons som bekreftelse på vellykket bestilling
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500  # Feil ved bestilling, returnerer feilbeskjed

# Starter Flask-applikasjonen når denne filen kjøres
if __name__ == '__main__':
    app.run(debug=True)
