import paho.mqtt.client as mqtt
import json
import time

values = (5, 1, 2, 'false', 'false')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("ack/message")

# def on_subscribe(client, userdata, mid, granted_qos):


def on_publish(client, userdata, mid):
    # print("on_publish")
    # time.sleep(3)
    message = json.dumps(values)  # Serializing Data
    client.publish("hello/world", message)
    # client.subscribe("ack/message")
    # print(mid)


i = 1
def on_message(client, userdata, msg):
    print("wdAWEqw" + str(i))
    ack_message = json.loads(msg.payload)
    print(ack_message)
    # if type(ack_message) is list:
    # while values[0] != ack_message:
    #    print()
    # print("ack access")


s_client = mqtt.Client()
s_client.on_message = on_message
s_client.on_publish = on_publish
s_client.on_connect = on_connect
s_client.connect("10.20.3.243", 1883, 60)

message = json.dumps(values)  # Serializing Data
s_client.publish("hello/wor", message)

s_client.loop_forever(5)  # timeout = 2s
