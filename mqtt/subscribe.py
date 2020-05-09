import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
env_path = './.env'
load_dotenv(dotenv_path=env_path)


class Subscriber:

    def __init__(self):
        self.topic = "test"
        self.BROKER_IP = str(os.getenv("MASTER_IP"))
        self.BROKER_PORT = int(os.getenv("BROKER_PORT"))

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connection established, returned code=", rc)
            client.subscribe(self.topic)
        else:
            print("connection error, returned code=", rc)

    def on_message(self, client, userdata, msg):
        print("topic: {} | payload: {} ".format(msg.topic, msg.payload))

    def on_log(self, client, userdata, level, buf):
        print("log ", buf)

    def subscribe(self):
        broker_address = self.BROKER_IP
        broker_port = self.BROKER_PORT
        print(broker_address)
        # initialise MQTT Client
        client = mqtt.Client("toagentpi")

        # binds functions defined above, on connection, message and log
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_log = self.on_log

        # client.username_pw_set(user, password)
        client.connect(broker_address, broker_port)
        client.loop_forever()
