import os
from flask import Flask, request
from kubernetes import client
import base64
from tempfile import NamedTemporaryFile
import os
import yaml
import string
import random

app = Flask(__name__)

HOST_URL = os.environ.get("HOST_URL")
CACERT = os.environ.get("CACERT")
TOKEN = os.environ.get("TOKEN")

configuration = client.Configuration()
with NamedTemporaryFile(delete=False) as cert:
    cert.write(base64.b64decode(CACERT))
    configuration.ssl_ca_cert = cert.name
configuration.host = HOST_URL
configuration.verify_ssl = True
configuration.debug = False
configuration.api_key = { "authorization": "Bearer {}".format(base64.b64decode(TOKEN).decode("utf-8")) }
client.Configuration.set_default(configuration)

v1 = client.BatchV1Api()

@app.route("/healthz")
def root():
    return "Working"

@app.route("/trigger/job1")
def trigger_job1():
    with open("job1.yaml") as file:
        body = yaml.safe_load(file)
        body['metadata']['name'] = "job1-{}".format(''.join(random.choices(string.ascii_lowercase, k = 5)))
        
    v1.create_namespaced_job(namespace="default", body=body, pretty=True)
    return "Job triggered!"

@app.route("/trigger/job2")
def trigger_job2():
    process_folder = request.args.get("folder")
    with open("job2.yaml") as file:
        body = yaml.safe_load(file)
        body['metadata']['name'] = "job2-{}".format(''.join(random.choices(string.ascii_lowercase, k = 5)))
        body['spec']['template']['spec']['containers'][0]['env'][0]['value'] = process_folder
        
    v1.create_namespaced_job(namespace="default", body=body, pretty=True)
    return "Job triggered!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)