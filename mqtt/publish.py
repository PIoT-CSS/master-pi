import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import logging
import os
from dotenv import load_dotenv
import hashlib
import time

load_dotenv()
env_path = './.env'
load_dotenv(dotenv_path=env_path)

##hashes
out_hash_md5 = hashlib.md5()
in_hash_md5 = hashlib.md5()

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
        self.topic = 'test'
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

    def send_header(self, client, filename, topic, qos):
        header="header"+",,"+filename+",,"
        header=bytearray(header,"utf-8")
        header.extend(b','*(200-len(header)))
        print(header)
        publish(client,topic,header,qos)

    def send_end(self, client, filename, topic, qos):
        end="end"+",,"+filename+",,"+out_hash_md5.hexdigest()
        end=bytearray(end,"utf-8")
        end.extend(b','*(200-len(end)))
        print(end)
        publish(client,topic,end,qos)

    def wait_for(self, client, msgType,period=0.25,wait_time=40,running_loop=False):
        client.running_loop=running_loop #if using external loop
        wcount=0  
        while True:
            #print("waiting"+ msgType)
            if msgType=="PUBACK":
                if client.on_publish:        
                    if client.puback_flag:
                        return True
        
            if not client.running_loop:
                client.loop(.01)  #check for messages manually
            time.sleep(period)
            #print("loop flag ",client.running_loop)
            wcount+=1
            if wcount>wait_time:
                print("return from wait loop taken too long")
                return False
        return True     

    def publish(self, payload, qos):
        # Create new instance
        client = mqtt.Client("toagentpi")
        client.on_publish = self.on_publish
        client.on_disconnect = self.on_disconnect
        client.on_connect = self.on_connect

        # Connect to pi
        client.connect(self.broker_address, self.port)

        # Publish to topic
        client.publish(self.topic, json.dumps(payload))
        client.disconnect() #disconnect
        client.loop_stop() #stop loop

    def file_publish(self, file_name, qos):
        
        client = mqtt.Client("toagentpi")
        payload = 'test'
        res,mid=client.publish(self.topic, payload, qos)
        
        if res==0: 
            if wait_for(client,"PUBACK", running_loop=True):
                if mid==client.mid_value:
                    print("match mid ",str(mid))
                    client.puback_flag=False #reset flag
                else:
                    raise SystemExit("not got correct puback mid so quitting")
                
            else:
                raise SystemExit("not got puback so quitting")

        # Setting up processing for publishing encoding
        topic = "test"
        start=time.time()
        Run_flag=True
        count=0
        qos=1
        filename="{}.pickles".format(file_name)
        send_header(client, filename, topic, qos)
        data_block_size=2000
        fo=open(filename,"rb")
        # fout=open("1out.txt","wb") #use a different filename

        while Run_flag:
            chunk=fo.read(data_block_size)
            if chunk:
                out_hash_md5.update(chunk)
                out_message=chunk
                #print(" length =",type(out_message))
                publish(client,topic,out_message,qos)
                    
            else:
                #send hash
                out_message=out_hash_md5.hexdigest()
                send_end(client, filename, topic, qos)
                #print("out Message ",out_message)
                res,mid=client.publish("data/files",out_message,qos=1)
                Run_flag=False
    
        fo.close()
            

