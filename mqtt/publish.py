import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import logging
import os
from dotenv import load_dotenv
load_dotenv()
env_path = './.env'
load_dotenv(dotenv_path=env_path)

BROKER_IP = os.getenv("AGENT_IP")
BROKER_PORT = os.getenv("BROKER_PORT")

'''
methods
- connect()
- disconnect()
- subscribe()
- publish ()
'''


class Publisher:
    
    def __init__(self):
        self.broker_address = str(BROKER_IP)
        self.port = int(BROKER_PORT)

    def on_publish(self, client, userdata, result):
        print("data published {} \n".format(result))
        pass

    def on_disconnect(self, client, userdata, rc):
        logging.debug("disconnected, rc=", str(rc))
        client.loop_stop()
        print("client disconnected OK")

    def on_connect(self, client, userdata, rc):
        print("client connected OK", str(rc))

    def publish(self, payload):
        # setting topic to publish to
        topic = "test"
        id = "id"
        payload_new = {'pi-id' : id, 'payload': payload}
        print(self.broker_address)
        # create new instance
        client = mqtt.Client("toagentpi")
        client.on_publish = self.on_publish
        client.on_disconnect = self.on_disconnect
        client.on_connect = self.on_connect
        
        # set broker address of raspberry pis
        # connect to pi
        client.connect(self.broker_address, self.port)
        #publish.single(topic, payload, self.broker_address) 
        # Publish to topic
        client.publish(topic, json.dumps(payload_new))
        client.disconnect()
            

