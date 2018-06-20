#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# greengrassSagemakerInference.py

import greengrasssdk
import platform
from threading import Timer
import time
import boto3
import cv2

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')
s3 = boto3.client('s3')

def greengrassSagemakerInference_run():
    vidcap=cv2.VideoCapture(0)
    vidcap.open(0)
    #sleep(1) this may be required if camera needs warm up.
    retval, image = vidcap.read()
    vidcap.release()
    # Sagemaker code is commented out for testing
    # endpoint_name = "your-endpoint"
    # runtime = boto3.Session().client(service_name='sagemaker-sagemaker',region_name='us-east-1')
    # response = runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/x-image', Body=image)
    # client.publish(topic='ModelInference', payload=response)
    response = s3.put_object(ACL='public-read',
                             Body=jpg_data.tostring(),
                             Bucket=bucket_name,
                             Key=key)
    push_to_s3(image,0)
    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(5, greengrassSagemakerInference_run).start()


# Execute the function above
greengrassSagemakerInference_run()

def push_to_s3(img, index):
    try:
        #Please change the bucket name to your bucket
        bucket_name = "sagemaker-iotlabjun202018"
        timestamp = int(time.time())
        now = datetime.datetime.now()
        key = "faces/{}_{}/{}_{}/{}_{}.jpg".format(now.month, now.day,now.hour, now.minute,timestamp, index)
        s3 = boto3.client('s3')
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, jpg_data = cv2.imencode('.jpg', img, encode_param)
        response = s3.put_object(ACL='public-read', Body=jpg_data.tostring(), Bucket=bucket_name, Key=key)
        client.publish(topic='ModelInference', payload="Response: {}".format(response))
        client.publish(topic='ModelInference', payload="Face pushed to S3")
    except Exception as e:
        msg = "Pushing to S3 failed: " + str(e)
        client.publish(topic='ModelInference', payload=msg)

# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
