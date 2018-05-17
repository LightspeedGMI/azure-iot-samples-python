from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import sys
import boto3

def updateDeviceState(device_seq, device_state):
    host = "a3mfkf3z93nqt8.iot.us-west-2.amazonaws.com"
    rootCAPath = "certs/root-CA.crt"
    certificatePath = "certs/team55device%s.cert.pem" % (device_seq+1)
    privateKeyPath = "certs/team55device%s.private.key" % (device_seq+1)
    clientId = "team55"

    thingName = "team55device%s" % (device_seq+1)

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


def device_state(low, high):
    return {"median": (low + high) / 2, "low_median": low, "high_median": high}


N = 1000000
num_devices = 2
low_median = 0
high_median = N
device_ids = range(0, num_devices)

if len(sys.argv) > 1 and 'init' == sys.argv[1]:
    if len(sys.argv) > 2:
        updateDeviceState(int(sys.argv[2]), device_state(low_median, high_median))
    else:
        for device_id in device_ids:
            updateDeviceState(device_id, device_state(low_median, high_median))
else:
    sqs_client = boto3.client('sqs')
    while True:

        approx_median = (low_median + high_median) / 2

        counts = {str(device_id+1): None for device_id in device_ids}

        while any([count is None for count in counts.values()]):
            messages = sqs_client.receive_message(QueueUrl='https://sqs.us-west-2.amazonaws.com/617297736688/hack1', MaxNumberOfMessages=10)
            if 'Messages' in messages:  # when the queue is exhausted, the response dict contains no 'Messages' key
                for message in messages['Messages']:  # 'Messages' is a list
                    # next, we delete the message from the queue so no one else will process it again
                    device_body = json.loads(message['Body'])
                    print(device_body)
                    counts[device_body['device']] = device_body['message']['counts']
                    print(list([count is None for count in counts.values()]))
                    sqs_client.delete_message(QueueUrl='https://sqs.us-west-2.amazonaws.com/617297736688/hack1', ReceiptHandle=message['ReceiptHandle'])
            time.sleep(5)

        lcount, ecount, hcount = 0, 0, 0
        for device_id, count in counts.iteritems():
            low, eq, high = count
            lcount += low
            hcount += high
            ecount += eq

        print(low_median, lcount, approx_median, ecount, hcount, high_median)

        if lcount < hcount:
            low_median = approx_median
        elif hcount < lcount:
            high_median = approx_median

        print("Median: " + str(approx_median))

        if approx_median == (low_median + high_median) / 2:
            if (ecount == 0) and ((lcount + hcount) % 2 == 0):
                print("Median %f: " % (low_median + high_median) / 2.0)
            else:
                print("Median %d: " % approx_median)
            break

        for device_id in device_ids:
            updateDeviceState(device_id, updateDeviceState(device_id, device_state(low_median, high_median)))

