import sqlite3

# Créez une connexion à la base de données SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Création de la table users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_prenom TEXT NOT NULL,
    date_naissance TEXT NOT NULL,
    annee_arrivee TEXT NOT NULL,
    email TEXT NOT NULL,
    etablissement TEXT NOT NULL,
    filiere TEXT NOT NULL,
    student_code TEXT UNIQUE NOT NULL,
    photo TEXT
)
''')

print("Table 'users' créée avec succès.")
conn.commit()
conn.close()
