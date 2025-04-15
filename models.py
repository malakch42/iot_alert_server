import mysql.connector
from datetime import datetime

# Fonction pour établir la connexion à la base de données
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="malak",               # Ton utilisateur MySQL
        password="malak2004",       # Ton mot de passe MySQL
        database="iot_alerts"
    )

# Fonction pour enregistrer une alerte dans la base de données
def enregistrer_alerte(type_alerte, valeur):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO alertes (type, valeur, timestamp) VALUES (%s, %s, %s)"
    val = (type_alerte, valeur, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()

# Fonction pour récupérer toutes les alertes (sous forme de dictionnaires)
def get_all_alertes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # ← Important !
    cursor.execute("SELECT id, type, valeur, timestamp FROM alertes ORDER BY timestamp DESC")
    alertes = cursor.fetchall()
    cursor.close()
    conn.close()
    return alertes

# Fonction pour récupérer des alertes filtrées par type
def get_filtered_alertes(type_alerte=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # ← Important aussi ici !
    
    if type_alerte:
        cursor.execute("SELECT id, type, valeur, timestamp FROM alertes WHERE type = %s ORDER BY timestamp DESC", (type_alerte,))
    else:
        cursor.execute("SELECT id, type, valeur, timestamp FROM alertes ORDER BY timestamp DESC")
    
    alertes = cursor.fetchall()
    cursor.close()
    conn.close()
    return alertes
