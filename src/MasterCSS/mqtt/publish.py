"""
publish.py contains mqtt publish logic for MP.
"""
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import logging
import os
from dotenv import load_dotenv
import hashlib
import time
import base64

load_dotenv()
env_path = './.env'
load_dotenv(dotenv_path=env_path)

# hashes
out_hash_md5 = hashlib.md5()
in_hash_md5 = hashlib.md5()

BROKER_IP = os.getenv("AGENT_IP")
BROKER_PORT = os.getenv("BROKER_PORT")


class Publisher:
    """
    Class that contains publish logic. when given a payload and route
    it will publish to the correct route.

    Methods
    -------
    __init__(self):
        initialises routes that it will publish to, ip address of AP and port.
    on_publish(self, client, userdata, result):
        function to run on successful publish
    on_disconnect(self, client, userdata, rc):
        function to run on disconnect
    on_connect(self, client, userdata, rc):
        function to run on connect
    publish(self, topic, payload, qos):
        initialises client and binds functions, publish received payload to AP at a given topic and disconnects.
    fr_publish(self, file_name, qos):
        initialises client and binds functions, publish user's image for facial recognition as payload to AP at a given topic and disconnects.
    send_end(self, client, filename, topic, qos):
        sends end of file to identify image sent for facial recognition
    send_header(self, client, filename, topic, qos):
        sends header to identify image sent for facial recognition
    convertImageToByteArray(self, file_name):
        converts user's image into byte array to be published
    """

    def __init__(self):
        """
        initialises routes that it will publish to, ip address of AP and port.
        """
        self.AUTH_RESP_FR_TOPIC = 'AUTH/RESP/FR'
        self.AUTH_RESP_UP_TOPIC = 'AUTH/RESP/UP'
        self.RETURN_TOPIC = 'RETURN'
        self.BROKER_ADDRESS = str(BROKER_IP)
        self.PORT = int(BROKER_PORT)

    def on_publish(self, client, userdata, result):
        """
        function to run on successful publish
        """
        print("data published {} \n".format(result))
        pass

    def on_disconnect(self, client, userdata, rc):
        """
        function to run on disconnect
        """
        logging.debug("disconnected, rc=", str(rc))
        client.loop_stop()
        print("client disconnected OK")

    def on_connect(self, client, userdata, rc):
        """
        function to run on connect
        """
        print("client connected OK", str(rc))

    def send_header(self, client, filename, topic, qos):
        """
        sends header to identify image sent for facial recognition
        """
        header = "header"+",,"+filename+",,"
        header = bytearray(header, "utf-8")
        header.extend(b','*(200-len(header)))
        print(header)
        client.publish(topic, header, qos)

    def send_end(self, client, filename, topic, qos):
        """
        sends end of file to identify image sent for facial recognition
        """
        end = "end"+",,"+filename+",,"+out_hash_md5.hexdigest()
        end = bytearray(end, "utf-8")
        end.extend(b','*(200-len(end)))
        print(end)
        client.publish(topic, end, qos)

    def publish(self, topic, payload, qos):
        """
        initialises client and binds functions, publish received payload to AP at a given topic and disconnects.
        """
        # Create new instance
        client = mqtt.Client("toagentpi")
        client.on_publish = self.on_publish
        client.on_disconnect = self.on_disconnect
        client.on_connect = self.on_connect

        # Connect to pi
        client.connect(self.BROKER_ADDRESS, self.PORT)

        # Publish to topic
        if topic == 'UP':
            client.publish(self.AUTH_RESP_UP_TOPIC, json.dumps(payload))
            client.disconnect()  # disconnect
            client.loop_stop()  # stop loop
        elif topic == 'FR':
            client.publish(self.AUTH_RESP_FR_TOPIC, json.dumps(payload))
            client.disconnect()
            client.loop_stop()
        elif topic == 'RET':
            client.publish(self.RETURN_TOPIC, json.dumps(payload))
            client.disconnect()
            client.loop_stop()

    def fr_publish(self, file_name, qos):
        """
        initialises client and binds functions, publish user's image for facial recognition as payload to AP at a given topic and disconnects.
        """
        # Attach callback functions, initiate client and connect to it
        client = mqtt.Client("toagentpi")
        client.on_publish = self.on_publish
        client.on_disconnect = self.on_disconnect
        client.on_connect = self.on_connect
        client.connect(self.BROKER_ADDRESS, self.PORT)

        # Sending header, to identify image
        self.send_header(client, file_name, self.AUTH_RESP_FR_TOPIC, qos)

        # Retrieve Image, and encode in Base64
        byteArr = self.convertImageToByteArray(file_name)

        # PublishEncodedImage
        print(" length =", type(byteArr))
        #client.publish(self.AUTH_RESP_FR_TOPIC, encoded)
        publish.single(self.AUTH_RESP_FR_TOPIC, byteArr,
                       hostname=self.BROKER_ADDRESS)
        print("DEBUG")

    def convertImageToByteArray(self, file_name):
        """
        converts user's image into byte array to be published
        """
        folder_name = 'src/MasterCSS/encoding/dataset'
        user_name = file_name
        dataset_directory = "./{}/{}/{}.jpg".format(
            folder_name, user_name, file_name)

        with open(dataset_directory, "rb") as image_file:
            img = image_file.read()
            byteArr = bytearray(img)

        return byteArr
