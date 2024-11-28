from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import uuid

# Configuration de l'application Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Route : formulaire d'inscription
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom_prenom = request.form['nom_prenom']
        date_naissance = request.form['date_naissance']
        annee_arrivee = request.form['annee_arrivee']
        email = request.form['email']
        etablissement = request.form['etablissement']
        filiere = request.form['filiere']

        # Génération automatique d'un code étudiant unique
        student_code = f"ETU-{uuid.uuid4().hex[:6].upper()}"

        # Gestion du fichier photo téléchargé
        photo = request.files['photo']
        photo_filename = None
        if photo and photo.filename != '':
            photo_filename = student_code + '_' + photo.filename
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        # Insertion dans la base de données
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (nom_prenom, date_naissance, annee_arrivee, email, etablissement, filiere, student_code, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nom_prenom, date_naissance, annee_arrivee, email, etablissement, filiere, student_code, photo_filename))
        conn.commit()
        conn.close()

        # Passer les données à la page de validation
        return render_template('validation.html', 
                               nom_prenom=nom_prenom,
                               date_naissance=date_naissance,
                               annee_arrivee=annee_arrivee,
                               email=email,
                               etablissement=etablissement,
                               filiere=filiere,
                               student_code=student_code,
                               photo=photo_filename)
    return render_template('form.html')


# Route : liste des utilisateurs
@app.route('/users')
def users():
    # Connexion à la base de données
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)


if __name__ == '__main__':
    # Crée le dossier d'uploads si nécessaire
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
