from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json


def updateDeviceState(device_seq, device_state):
    host = "a3mfkf3z93nqt8.iot.us-west-2.amazonaws.com"
    rootCAPath = "certs/root-CA.crt"
    certificatePath = "certs/team55device%s.cert.pem" % device_seq
    privateKeyPath = "certs/team55device%s.private.key" % device_seq
    clientId = "team55"

    thingName = "team55device%s" % device_seq

    # Custom Shadow callback
    def customShadowCallback_Update(payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        if responseStatus == "timeout":
            print("Update request " + token + " time out!")
        if responseStatus == "accepted":
            payloadDict = json.loads(payload)
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Update request with token: " + token + " accepted!")
            print("property: " + json.dumps(payloadDict["state"]["desired"]))
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if responseStatus == "rejected":
            print("Update request " + token + " rejected!")

    def customShadowCallback_Delete(payload, responseStatus, token):
        if responseStatus == "timeout":
            print("Delete request " + token + " time out!")
        if responseStatus == "accepted":
            print("~~~~~~~~~~~~~~~~~~~~~~~")
            print("Delete request with token: " + token + " accepted!")
            print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if responseStatus == "rejected":
            print("Delete request " + token + " rejected!")

    # logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    # Init AWSIoTMQTTShadowClient
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTShadowClient configuration
    myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

    myAWSIoTMQTTShadowClient.connect()

    # Create a deviceShadow with persistent subscription
    deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)

    # Delete shadow JSON doc
    deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

    deviceShadowHandler.shadowUpdate(json.dumps({"state": {"desired": device_state}}), customShadowCallback_Update, 5)

    time.sleep(5)

    myAWSIoTMQTTShadowClient.disconnect()


updateDeviceState(1, {"range": [0, 1000000]})
updateDeviceState(2, {"range": [0, 1000000]})
# updateDeviceState(3, {"range": [0, 1000000]})
# updateDeviceState(4, {"range": [0, 1000000]})
# updateDeviceState(5, {"range": [0, 1000000]})
# updateDeviceState(6, {"range": [0, 1000000]})
