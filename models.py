import mysql.connector
from datetime import datetime

# Fonction pour établir la connexion à la base de données
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="malak",        # Remplace si tu utilises un autre utilisateur
        password="malak2004",        # Mets ton mot de passe MySQL si nécessaire
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

# Fonction pour récupérer toutes les alertes
def get_all_alertes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, valeur, timestamp FROM alertes ORDER BY timestamp DESC")
    alertes = cursor.fetchall()
    cursor.close()
    conn.close()
    return alertes

#filtrage 

def get_filtered_alertes(type_alerte=None):
    conn = get_connection()
    cursor = conn.cursor()

    if type_alerte:
        cursor.execute("SELECT * FROM alertes WHERE type = %s", (type_alerte,))
    else:
        cursor.execute("SELECT * FROM alertes")

    alertes = cursor.fetchall()
    cursor.close()
    conn.close()
    return alertes

