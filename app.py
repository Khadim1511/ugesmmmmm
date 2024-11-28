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

# Configuration de la base de données PostgreSQL
DATABASE_URL = os.getenv('postgresql://recen_user:KRfg6g6AzqfoANjQHJC2xlaRWaLIqkSO@dpg-ct3s062j1k6c73ebpdog-a.oregon-postgres.render.com/recen')

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
    """Génère un code étudiant unique de 8 caractères."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

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

    # Générer un code étudiant unique
    student_code = generate_student_code()

    # Gérer le téléchargement de la photo
    photo = request.files['photo']
    photo_filename = None
    if photo:
        photo_filename = f"{nom_prenom.replace(' ', '_')}_{photo.filename}"
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

    # Insérer dans la base de données PostgreSQL
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
                           photo=photo_filename)

# Route pour afficher tous les utilisateurs
@app.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
