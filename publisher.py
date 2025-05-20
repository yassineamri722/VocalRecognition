import paho.mqtt.client as mqtt

BROKER = "rude-houses-accept.loca.lt"  # IP PUBLIQUE DE TON AMI
PORT = 8883  # Port MQTT

client = mqtt.Client()

client.connect(BROKER, PORT)

# Publier un message sur le topic "assistant/request"
client.publish("assistant/request", "Quel est l'heure actuelle ?")

print("Message envoyé !")

client.disconnect()
