# simulateur.py
import paho.mqtt.publish as publish
import json
import time
import random

MQTT_BROKER = "localhost"
TOPIC = "capteurs/alertes"

types_alertes = ["fumee", "gaz", "temperature", "inondation", "mouvement"]

# Délais personnalisés pour chaque type d'alerte (en secondes)
delais_par_type = {
    "fumee": 10,
    "gaz": 12,
    "temperature": 8,
    "inondation": 15,
    "mouvement": 3
}

while True:
    type_alerte = random.choice(types_alertes)
    valeur = 1  # On suppose que 1 = alerte déclenchée

    message = {
        "type": type_alerte,
        "valeur": valeur
    }

    try:
        publish.single(TOPIC, json.dumps(message), hostname=MQTT_BROKER)
        print("✅ Message MQTT envoyé :", message)
    except Exception as e:
        print("❌ Erreur d'envoi MQTT :", e)

    # Pause personnalisée selon le type d'alerte
    time.sleep(delais_par_type[type_alerte])
