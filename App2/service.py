import os
from google.cloud import storage

GCS_BUCKET_PROCESS_1 = "dev-trials-q-process-1"
GCS_BUCKET_PROCESS_2 = "dev-trials-q-process-2"

def download_folder(foldername, folderpath):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_PROCESS_1)
    blobs = bucket.list_blobs(prefix=foldername)

    if not os.path.exists(folderpath):
        os.mkdir(folderpath)

    for blob in blobs:
        filename = blob.name.replace(foldername, "").replace("/","")
        blob.download_to_filename(os.path.join(folderpath, filename))
        print("Downloaded file: {}".format(blob.name))
    print("\nFiles Downloaded!\n")

def modify_files(foldername, folderpath):
    for filename in os.listdir(folderpath):
        with open(os.path.join(folderpath, filename), "a") as file:
            print("Modifying file: {}".format(filename))
            file.write("\n{}".format(filename))
        file.close()
    print("\nFiles Modified!\n")

def upload_files(foldername, folderpath):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_PROCESS_2)

    for filename in os.listdir(folderpath):
        blob = bucket.blob("{}/{}".format(foldername, filename))
        blob.upload_from_filename(os.path.join(folderpath, filename))
        print("File {} uploaded to {}".format(os.path.join(folderpath, filename), "{}/{}".format(foldername, filename)))
    
    print("\nFiles Uploaded!\n")

def main():
    foldername = os.environ.get("PROCESS_FOLDER")
    folderpath = os.path.join(".\\", foldername)
    print("\nDOWNLOADING FILES!\n")
    download_folder(foldername, folderpath)
    print("\nMODIFYING FILES!\n")
    modify_files(foldername, folderpath)
    print("\nUPLOADING FILES!\n")
    upload_files(foldername, folderpath)
    print("\nCOMPLETED!\n")

if __name__ == "__main__":
    main()