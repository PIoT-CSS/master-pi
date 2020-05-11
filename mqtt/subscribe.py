import paho.mqtt.client as mqtt
from mqtt.publish import *
import json
import os
from dotenv import load_dotenv
env_path = './.env'
load_dotenv(dotenv_path=env_path)


class Subscriber:
    """
    A class to initiate a subscriber via MQTT topic

    Methods
    -------
    subscribe(self):
        Initiates a MQTT Client, connects and listens for publishes to a specified topic
    on_connect(self, client, userdata, flags, rc):
        A callback function that is called when the client connects to a broker, a specified address.


    """
    def __init__(self):
        self.AUTH_FR_TOPIC = "AUTH/FR"
        self.AUTH_UP_TOPIC = "AUTH/UP"
        self.BROKER_IP = str(os.getenv("MASTER_IP"))
        self.BROKER_PORT = int(os.getenv("BROKER_PORT"))

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connection established, returned code=", rc)
            client.subscribe(self.AUTH_FR_TOPIC)
            client.subscribe(self.AUTH_UP_TOPIC)

        else:
            print("connection error, returned code=", rc)

    def on_message(self, client, userdata, msg):
        print("topic: {} | payload: {} ".format(msg.topic, msg.payload))
        if msg.topic == 'AUTH/FR':
            print("[DEBUG] issues with creating a publisher")
            pub = Publisher()
            print("[DEBUG] tried to publish")
            pub.file_publish('alex', 1)
        elif msg.topic == 'AUTH/UP':
            pub = Publisher()


    def on_log(self, client, userdata, level, buf):
        print("log ", buf)

    def subscribe(self):
        broker_address = self.BROKER_IP
        broker_port = self.BROKER_PORT
        
        # initialise MQTT Client
        client = mqtt.Client("toagentpi")

        # binds functions defined above, on connection, message and log
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_log = self.on_log

        # client.username_pw_set(user, password)
        client.connect(broker_address, broker_port)
        client.loop_forever()
