import time
from concurrent.futures import ThreadPoolExecutor
from botocore.client import Config
import boto3
import requests
from io import BytesIO
vakuumsensor_url = "http://10.255.255.254:2043/"
s3_host = "http://10.255.255.254:2016/"
bucket_name = "analyzer-gamma"
file_name = "data.hex"
access_key = "theship"
secret_key = "theship1234"

def measure(direction):
    try:
        response = requests.post(url=vakuumsensor_url + direction + "/measure", timeout=5)
        data = response.json()
        if "measurement" in data:
            return data["measurement"]
    except Exception as e:
        print(f"Error in direction {direction}: {e}")
    return None

def get_antimateria_data():
    with ThreadPoolExecutor(max_workers=3) as executor:
        responses = [executor.submit(measure, d) for d in ["x", "y", "z"]]

        for response in responses:
            result = response.result()
            if result:
                print("Measurement:", result)
                return result

    print("No measurement returned.")
    return None

def write_to_s3_storage(msg):
    s3 = boto3.client('s3',
                      endpoint_url=s3_host,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key
                      )
    file_content = msg.encode("utf-8")
    file_obj = BytesIO(file_content)

    s3.upload_fileobj(file_obj, bucket_name, file_name)

while True:
    msg = get_antimateria_data()
    if msg is not None:
        write_to_s3_storage(msg)
    time.sleep(2)