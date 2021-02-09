import base64
import requests

def trigger_job(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print("Folder to process: {}".format(pubsub_message))
    response = requests.get("http://35.193.45.139/trigger/job2?folder={}".format(pubsub_message))

    print("Response Status Code: {}".format(response.status_code))