import paho.mqtt.client as mqtt

BROKER = "rude-houses-accept.loca.lt"  # Mosquitto tourne en local
PORT = 8883

def on_message(client, userdata, message):
    request = message.payload.decode()
    print(f"Message reçu: {request}")

    # Répondre avec un message simulé
    if "heure" in request:
        response = "Il est 14h30."
    else:
        response = "Je ne comprends pas."

    client.publish("assistant/response", response)

client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe("assistant/request")

print("En attente de messages...")
client.loop_forever()
