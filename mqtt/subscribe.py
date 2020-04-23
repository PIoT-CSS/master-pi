
import paho.mqtt.client as mqtt
import json
import os
import utility.loadconfig as loadconfig
from dotenv import load_dotenv
env_path = './.env'
load_dotenv(dotenv_path=env_path)


class Subscriber:

    def __init__(self):
        self.topic = "test"
        self.BROKER_IP = os.getenv("BROKER_IP")
        self.BROKER_PORT = os.getenv("BROKER_PORT")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connection established, returned code=", rc)
            client.subscribe(self.topic)
        else:
            print("connection error, returned code=", rc)

    def on_message(self, client, userdata, msg):
        print("topic: {} | payload: {} ".format(msg.topic, msg.payload))
        payload = {"message": "On"}
        client.publish(self.topic, json.dumps(payload))

    def on_log(self, client, userdata, level, buf):
        print("log ", buf)

    def subscribe(self):
        
