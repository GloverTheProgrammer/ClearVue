import requests

def download_file(url, destination_folder):
    local_filename = url.split('/')[-1]
    path = f"{destination_folder}/{local_filename}"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

# URLs of the model and its preprocessing config to download
model_url = "https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/object_detection/rpi/lite-model_efficientdet_lite0_detection_metadata_1.tflite"

# Destination folder
destination_folder = "models"

# Download the model and its preprocessing config
download_file(model_url, destination_folder)
