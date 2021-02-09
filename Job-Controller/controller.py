import os
from flask import Flask
from kubernetes import client
import base64
from tempfile import NamedTemporaryFile
import os
import yaml

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
configuration.api_key = { "authorization": "Bearer " + TOKEN }
client.Configuration.set_default(configuration)

v1 = client.BatchV1Api()

@app.route("/healthz")
def root():
    return "Working"

@app.route("/trigger/job1")
def trigger_job1():
    with open("job1.yaml") as file:
        body = yaml.safe_load(file)
        
    v1.create_namespaced_job(namespace="default", body=body, pretty=True)
    return "Job triggered!"

@app.route("/trigger/job2")
def trigger_job2():
    with open("job2.yaml") as file:
        body = yaml.safe_load(file)
        
    v1.create_namespaced_job(namespace="default", body=body, pretty=True)
    return "Job triggered!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)