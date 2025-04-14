import json
import paho.mqtt.client as mqtt
from models import enregistrer_alerte  # Ce fichier doit exister

# Connexion au broker MQTT
def on_connect(client, userdata, flags, rc):
    print("[MQTT] Connecté avec le code de résultat", rc)
    client.subscribe("capteurs/#")  # S'abonner à tous les topics commençant par "capteurs/"

# Traitement des messages MQTT
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"[MQTT] Message reçu sur {msg.topic} : {payload}")

        type_alerte = payload.get("type")
        valeur = payload.get("valeur")

        if type_alerte and valeur is not None:
            print(f"📥 Alerte reçue : {type_alerte} = {valeur}")

            # Affichage personnalisé selon le type
            if type_alerte == "fumee":
                print("🚨 Alerte fumée détectée !")
            elif type_alerte == "temperature" and int(valeur) > 50:
                print("🌡️ Température élevée !")
            elif type_alerte == "gaz":
                print("🧪 Gaz détecté !")
            elif type_alerte == "inondation":
                print("💧 Risque d'inondation !")
            elif type_alerte == "mouvement":
                print("👣 Mouvement détecté !")

            # Enregistrement dans la base de données
            enregistrer_alerte(type_alerte, str(valeur))
        else:
            print("❌ Type ou valeur manquants :", payload)

    except Exception as e:
        print(f"[ERREUR] Impossible de traiter le message MQTT : {e}")

# Démarrage du client MQTT
def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    client.loop_forever()

# Lancement
if __name__ == "__main__":
    start_mqtt_client()
