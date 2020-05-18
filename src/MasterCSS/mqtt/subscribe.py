import paho.mqtt.client as mqtt
from MasterCSS.mqtt.publish import *
from MasterCSS.controllers.car import pickup_car, return_car
from MasterCSS.controllers.auth import verify_login
import json
import os
from dotenv import load_dotenv
env_path = './.env'
load_dotenv(dotenv_path=env_path)

BROKER_IP = os.getenv("MASTER_IP")
BROKER_PORT = os.getenv("BROKER_PORT")

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
        self.RETURN_TOPIC = "RETURN"
        self.BROKER_ADDRESS = str(BROKER_IP)
        self.BROKER_PORT = int(BROKER_PORT)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connection established, returned code=", rc)
            client.subscribe(self.AUTH_FR_TOPIC)
            client.subscribe(self.AUTH_UP_TOPIC)
            client.subscribe(self.RETURN_TOPIC)
        else:
            print("connection error, returned code=", rc)

    def on_message(self, client, userdata, msg):
        print("topic: {} | payload: {} ".format(msg.topic, msg.payload))
        payload = json.loads(msg.payload)
        if msg.topic == 'AUTH/FR':
            if pickup_car(payload['username']):
                print("[DEBUG] issues with creating a publisher")
                pub = Publisher()
                print("[DEBUG] tried to publish", msg.payload)
                pub.fr_publish(payload['username'], 1)
        elif msg.topic == 'AUTH/UP':
            if verify_login(payload['username'], payload['pass']):
                if pickup_car(payload['username']):
                    pub = Publisher()
                    pub.publish('UP', 'Unlocked', 1)
        elif msg.topic == 'RETURN':
            if return_car(payload['username']):
                pub = Publisher()
                pub.publish('RET','Returned', 1)

    def on_log(self, client, userdata, level, buf):
        print("log ", buf)
    
    def subscribe(self):
        broker_address = self.BROKER_ADDRESS
        broker_port = self.BROKER_PORT
        
        # initialise MQTT Client
        client = mqtt.Client("toagentpi")

        # binds functions defined above, on connection, message and log
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_log = self.on_log

        client.connect(broker_address, broker_port)
        client.loop_forever()
