from flask import Flask, jsonify, request, render_template
from mqtt_client import start_mqtt_client
from models import get_all_alertes, get_filtered_alertes, enregistrer_alerte
import threading

app = Flask(__name__)

# Page d'accueil JSON
@app.route('/')
def index():
    return jsonify({"message": "Bienvenue sur le serveur IoT d'alerte !"})

# Endpoint pour afficher les alertes (JSON ou filtré par type)
@app.route('/alertes', methods=['GET'])
def lister_alertes():
    type_alerte = request.args.get('type')
    if type_alerte:
        alertes = get_filtered_alertes(type_alerte)
    else:
        alertes = get_all_alertes()
    return jsonify(alertes)

# Page HTML pour afficher les alertes
@app.route('/alertes_page')
def afficher_alertes():
    type_alerte = request.args.get('type')
    if type_alerte:
        alertes = get_filtered_alertes(type_alerte)
    else:
        alertes = get_all_alertes()
    return render_template("alertes.html", alertes=alertes)

# 🚨 Endpoint appelé par l’app Flutter
@app.route('/declencher_alerte', methods=['POST'])
def declencher_alerte():
    data = request.get_json()
    type_alerte = data.get('type')
    valeur = data.get('valeur')

    print(f"🚨 Alerte reçue depuis Flutter ! Type: {type_alerte}, Valeur: {valeur}")

    if not type_alerte or not valeur:
        return jsonify({"error": "Champs 'type' et 'valeur' requis"}), 400

    enregistrer_alerte(type_alerte, valeur)
    return jsonify({"message": "Alerte enregistrée avec succès"}), 201

# Démarrage du serveur Flask avec MQTT dans un thread
if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    print("✅ Serveur Flask en cours de démarrage...")
    app.run(host='0.0.0.0', port=5000, debug=True)
