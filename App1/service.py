import os
import datetime
from google.cloud import storage
from google.cloud import pubsub_v1

GCP_PROJECT = "dev-trials-q"
GCS_BUCKET = "dev-trials-q-process-1"
GCP_TOPIC = "gke-chain-job-trigger"

def generate_file(filename, content):
    with open(filename, "a") as file:
        file.write(content)
    file.close()

def write_files(folderpath):
    if not os.path.exists(folderpath):
        os.mkdir(os.path.join(folderpath))
        
    for i in range(1,101):
        filename = os.path.join(folderpath, "file-{}.txt").format(str(i))
        generate_file(filename, "content {}".format(str(i)))
        print("Generated file: {}".format(filename))
    
    print("\nFiles Generated!\n")

def upload_folder(bucket_name, foldername, folderpath):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for filename in os.listdir(folderpath):
        blob = bucket.blob("{}/{}".format(foldername, filename))
        blob.upload_from_filename(os.path.join(folderpath, filename))
        print("File {} uploaded to {}".format(os.path.join(folderpath, filename), "{}/{}".format(foldername, filename)))
    
    print("\nFiles Uploaded!\n")

def publish_message(foldername):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GCP_PROJECT, GCP_TOPIC)
    publisher.publish(topic_path, foldername.encode("utf-8"))
    print("\nPUBLISHED!\n")

def main():
    now = datetime.datetime.now()
    foldername = "{}-{}-{}_{}-{}-{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    folderpath = os.path.join(".", foldername)
    print("\nGenerating Files!\n")
    write_files(folderpath)
    print("\nUploading Files!\n")
    upload_folder(GCS_BUCKET, foldername, folderpath)
    publish_message(foldername)
    print("\nCOMPLETED!!")

if __name__ == "__main__":
    main()