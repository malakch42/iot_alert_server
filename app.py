from flask import Flask, jsonify, request
from mqtt_client import start_mqtt_client  # Import de la fonction pour démarrer MQTT
from models import get_all_alertes, get_filtered_alertes
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Bienvenue sur le serveur IoT d'alerte !"})

@app.route('/alertes', methods=['GET'])
def lister_alertes():
    type_alerte = request.args.get('type')  # récupère ?type= depuis l'URL
    if type_alerte:
        alertes = get_filtered_alertes(type_alerte)
    else:
        alertes = get_all_alertes()

    return jsonify(alertes)

if __name__ == '__main__':
    start_mqtt_client()  # Démarre MQTT dans un thread séparé
    print("✅ Serveur Flask en cours de démarrage...")
    app.run(host='0.0.0.0', port=5000, debug=True)  # Démarre Flask sur toutes les interfaces réseau
