from flask import Flask, render_template, request

app = Flask(__name__)

# Rute for kontaktsiden (hjemmeside)
@app.route("/", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        # Henter data fra kontaktskjemaet
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        print(f"Navn: {name}, E-post: {email}, Melding: {message}")

    return render_template("contact.html")  # Vist hvis GET-metode brukes, viser kontaktskjemaet


# Starter Flask-applikasjonen
if __name__ == "__main__":
    app.run(debug=True)
