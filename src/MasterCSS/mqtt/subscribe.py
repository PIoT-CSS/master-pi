"""
subscribe.py contains mqtt subscribe logic for MP.
"""
import paho.mqtt.client as mqtt
from MasterCSS.mqtt.publish import *
from MasterCSS.controllers.car import pickup_car, return_car
from MasterCSS.controllers.auth import verify_login, get_mac_addresses
from MasterCSS.controllers.issue import handle_resolve_issue
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
    """

    def __init__(self):
        """
        initialises the topic routes which it will listen to, ip address,
        port, username.
        """
        self.AUTH_FR_TOPIC = "AUTH/FR"
        self.AUTH_UP_TOPIC = "AUTH/UP"
        self.RETURN_TOPIC = "RETURN"
        self.ENG_TOPIC = "ENG"
        self.MAC_ADDR_REQ_TOPIC = "REQ/MAC_ADDR"
        self.BROKER_ADDRESS = str(BROKER_IP)
        self.BROKER_PORT = int(BROKER_PORT)

    def on_connect(self, client, userdata, flags, rc):
        """
        A callback function that is called when the client
        connects to a broker, a specified address

        :param client: the client instance for this callback
        :type client: Client

        :param userdata: the private user data as
        set in Client() or user_data_set()
        :type userdata: any

        :param flags: response flags sent by the broker
        :type flags: dict

        :param rc: result of connection
        :type rc: integer
        """
        if rc == 0:
            print("[MQTT RES]  connection established, returned code=", rc)
            client.subscribe(self.AUTH_FR_TOPIC)
            client.subscribe(self.AUTH_UP_TOPIC)
            client.subscribe(self.RETURN_TOPIC)
            client.subscribe(self.ENG_TOPIC)
            client.subscribe(self.MAC_ADDR_REQ_TOPIC)
        else:
            print("[MQTT RES]  connection error, returned code=", rc)

    def on_message(self, client, userdata, msg):
        """
        handles unlock/return car logic when receiving payload at
        a given topic

        :param client: the client instance for this callback
        :type client: Client

        :param userdata: the private user data as set in Client()
        or user_data_set()
        :type userdata: any

        :param msg: an instance of MQTTMessage. This is a class with members
        topic, payload, qos, retain.
        :type msg: MQTTMessage
        """
        print("[MQTT RES]  Payload received on topic: {}".format(msg.topic))
        payload = json.loads(msg.payload)
        pub = Publisher()
        if msg.topic == 'AUTH/FR':
            if payload['type'] == 'Encode Face':
                pub.fr_publish(payload['username'], 1)
            elif payload['type'] == 'Unlock':
                if pickup_car(payload):
                    pub.publish('FR', 'Unlocked', 1)
                else:
                    pub.publish('FR', 'Car unlock failed', 1)
        elif msg.topic == 'AUTH/UP':
            if verify_login(payload['username'], payload['pass']):
                if pickup_car(payload):
                    pub.publish('UP', 'Unlocked', 1)
                    return
            pub.publish('UP', 'Authentication denied', 1)
        elif msg.topic == 'RETURN':
            if return_car(payload):
                pub.publish('RET', 'Returned', 1)
            else:
                pub.publish('RET', 'Return denied', 1)
        elif msg.topic == 'ENG':
            # parsing to json again due to incomplete deserialisation
            payload = json.loads(payload)
            handle_resolve_issue(payload['ID'], payload['IssueID'])
        elif msg.topic == 'REQ/MAC_ADDR':
            pub.publish('MAC', get_mac_addresses(), 1)

    def on_log(self, client, userdata, level, buf):
        """
        Support function run for logging

        :param client: the client instance for this callback
        :type client: Client

        :param userdata: the private user data as set in Client() or
        user_data_set()
        :type userdata: any

        :param level: severity of the message
        :type level: MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING,
        MQTT_LOG_ERR, MQTT_LOG_DEBUG

        :param buf: message buffer
        :type buf: bytes
        """
        print("[MQTT LOG] ", buf)

    def subscribe(self):
        """
        Initiates a MQTT Client, connects and listens for publishes to a
        specified topic
        """
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
