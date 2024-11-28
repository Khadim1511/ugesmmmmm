from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import random
import string
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

DATABASE_URL = os.getenv("DATABASE_URL")

# Fonction pour obtenir une connexion à la base de données
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# Créer la table si elle n'existe pas
def create_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            nom_prenom TEXT NOT NULL,
            date_naissance TEXT NOT NULL,
            annee_arrivee TEXT NOT NULL,
            email TEXT NOT NULL,
            etablissement TEXT NOT NULL,
            filiere TEXT NOT NULL,
            student_code TEXT NOT NULL UNIQUE,
            photo TEXT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

create_database()

# Fonction pour générer un code étudiant unique
def generate_student_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return code

# Route pour afficher le formulaire
@app.route('/')
def index():
    return render_template('form.html')

# Route pour traiter le formulaire
@app.route('/submit', methods=['POST'])
def submit():
    nom_prenom = request.form['nom_prenom']
    date_naissance = request.form['date_naissance']
    annee_arrivee = request.form['annee_arrivee']
    email = request.form['email']
    etablissement = request.form['etablissement']
    filiere = request.form['filiere']
    student_code = generate_student_code()

    photo = request.files['photo']
    photo_filename = None
    if photo:
        photo_filename = f"{nom_prenom.replace(' ', '_')}_{photo.filename}"
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (nom_prenom, date_naissance, annee_arrivee, email, etablissement, filiere, student_code, photo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (nom_prenom, date_naissance, annee_arrivee, email, etablissement, filiere, student_code, photo_filename))
    conn.commit()
    cursor.close()
    conn.close()

    return render_template('validation.html', 
                           nom_prenom=nom_prenom, 
                           date_naissance=date_naissance, 
                           annee_arrivee=annee_arrivee, 
                           email=email, 
                           etablissement=etablissement, 
                           filiere=filiere, 
                           student_code=student_code, 
 
