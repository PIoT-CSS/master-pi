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

#load_dotenv()
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
    """

    def __init__(self):
        """
        initialises routes that it will publish to, ip address of AP and port.
        """
        self.AUTH_RESP_FR_TOPIC = 'AUTH/RESP/FR'
        self.AUTH_RESP_UP_TOPIC = 'AUTH/RESP/UP'
        self.RETURN_TOPIC = 'RETURN'
        self.MAC_ADDR_RESP_TOPIC = 'REQ/RESP/MAC_ADDR'
        self.BROKER_ADDRESS = str(BROKER_IP)
        self.PORT = int(BROKER_PORT)

    def on_publish(self, client, userdata, result):
        """
        callback function to run on successful publish

        :param client: the client instance for this callback
        :type client: Client

        :param userdata: the private user data as set in Client()
        or user_data_set()
        :type userdata: [type]

        :param result: Data being published
        :type result: String
        """
        print("[MQTT RES]  data published {} \n".format(result))
        pass

    def on_disconnect(self, client, userdata, rc):
        """
        function to run on disconnect

        :param client: the mqtt client
        :type client: Client

        :param userdata: the private user data as set in Client()
        or user_data_set()
        :type userdata: [type]

        :param rc: disconnection result
        :type rc: int
        """
        logging.debug("disconnected, rc=", str(rc))
        client.loop_stop()
        print("[MQTT RES]  client disconnected OK")

    def on_connect(self, client, userdata, rc):
        """
        callback function to run on_connect

        :param client: the mqtt client
        :type client: Client

        :param userdata: the private user data as set in Client()
        or user_data_set()
        :type userdata: [type]

        :param rc: connection result
        :type rc: int
        """
        print("[MQTT RES]  client connected OK", str(rc))

    def send_header(self, client, filename, topic, qos):
        """
        sends header to identify image sent for facial recognition

        :param client: sends header to identify image
        sent for facial recognition
        :type client: Client

        :param filename: name of the file that's being sent
        :type filename: string

        :param topic: topic to publish to
        :type topic: string

        :param qos: quality of service level to use
        :type qos: integer
        """
        header = "header"+",,"+filename+",,"
        header = bytearray(header, "utf-8")
        header.extend(b','*(200-len(header)))
        client.publish(topic, header, qos)

    def send_end(self, client, filename, topic, qos):
        """
        sends end of file to identify image sent for facial recognition

        :param client: sends header to identify image sent
        for facial recognition
        :type client: Client

        :param filename: name of the file that's being sent
        :type filename: string

        :param topic: topic to publish to
        :type topic: string

        :param qos: quality of service level to use
        :type qos: integer
        """
        end = "end"+",,"+filename+",,"+out_hash_md5.hexdigest()
        end = bytearray(end, "utf-8")
        end.extend(b','*(200-len(end)))
        client.publish(topic, end, qos)

    def publish(self, topic, payload, qos):
        """
        initialises client and binds functions, publish received payload to AP
         at a given topic and disconnects.

        :param topic: topic to publish to
        :type topic: string

        :param payload: the item that's being sent,
        will be converted into json.
        :type payload: any

        :param qos: quality of service level to use
        :type qos: integer
        """
        # Create new instance
        client = mqtt.Client("toagentpi")
        client.on_publish = self.on_publish
        client.on_disconnect = self.on_disconnect
        client.on_connect = self.on_connect

        # Connect to pi
        print("[MQTT RES]  Publishing to " + self.BROKER_ADDRESS)
        client.connect(self.BROKER_ADDRESS, self.PORT)

        # Publish to topic
        if topic == 'UP':
            client.publish(self.AUTH_RESP_UP_TOPIC, json.dumps(payload))
            client.disconnect()
            client.loop_stop()
        elif topic == 'FR':
            client.publish(self.AUTH_RESP_FR_TOPIC, json.dumps(payload))
            client.disconnect()
            client.loop_stop()
        elif topic == 'RET':
            client.publish(self.RETURN_TOPIC, json.dumps(payload))
            client.disconnect()
            client.loop_stop()
        elif topic == 'MAC':
            client.publish(self.MAC_ADDR_RESP_TOPIC, json.dumps(payload))
            client.disconnect()
            client.loop_stop()

    def fr_publish(self, file_name, qos):
        """
        initialises client and binds functions, publish user's image
         for facial recognition as payload to AP at a given topic
         and disconnects.

        :param file_name: filename being published
        :type file_name: string

        :param qos: quality of service level to use
        :type qos: integer
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
        publish.single(self.AUTH_RESP_FR_TOPIC, byteArr,
                       hostname=self.BROKER_ADDRESS)

    def convertImageToByteArray(self, file_name):
        """
        converts user's image into byte array to be published
        :return: bytes of the image
        :rtype: array of bytes
        """
        folder_name = 'src/MasterCSS/encoding/dataset'
        user_name = file_name
        dataset_directory = "./{}/{}/{}.jpg".format(
            folder_name, user_name, file_name)

        with open(dataset_directory, "rb") as image_file:
            img = image_file.read()
            byteArr = bytearray(img)

        return byteArr
