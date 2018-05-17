from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import logging
import time
import json
import sys

device_seq = sys.argv[1]

host = "a3mfkf3z93nqt8.iot.us-west-2.amazonaws.com"
rootCAPath = "certs/root-CA.crt"
certificatePath = "certs/team55device%s.cert.pem" % device_seq
privateKeyPath = "certs/team55device%s.private.key" % device_seq
clientId = "team55"

thingName = "team55device%s" % device_seq

# logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# the client
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing

myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Init AWSIoTMQTTShadowClient
myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

myAWSIoTMQTTShadowClient.connect()

deviceState = {}


def customShadowCallback_Delta(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    print(responseStatus)
    payloadDict = json.loads(payload)
    print("++++++++DELTA++++++++++")
    print("state: " + str(payloadDict["state"]))
    print("version: " + str(payloadDict["version"]))
    print("+++++++++++++++++++++++\n\n")
    deviceState.update(payloadDict["state"])


def customShadowCallback_Get(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    print(payload)
    print(responseStatus)
    print("++++++++GET++++++++++")
    try:
        payloadDict = json.loads(payload)
        print("state: " + str(payloadDict["state"]))
        print("version: " + str(payloadDict["version"]))
        print("+++++++++++++++++++++++\n\n")
        deviceState.update(payloadDict["state"])
    except Exception as e:
        print(str(e))


# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)

# Listen on deltas
# deviceShadowHandler.shadowRegisterDeltaCallback(customShadowCallback_Delta)

deviceShadowHandler.shadowGet(customShadowCallback_Get, 5)

time.sleep(10)

myAWSIoTMQTTClient.connect()

topic = "sdk/test/team55"
loopCount = 0

# Loop forever to react to device state delta requests
while True:
    message = {"msg": "INIT", "seq": loopCount}
    loopCount += 1
    messageJson = json.dumps({'message': message, 'device': device_seq})
    print(messageJson)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    time.sleep(5)
