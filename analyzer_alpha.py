import grpc
from concurrent import futures
import time
import uuid
import requests

import analyzer_alpha_pb2_grpc
import analyzer_alpha_pb2
vakuumsensor_url = "http://10.255.255.254:2037"


def get_measure_data():
    id = str(uuid.uuid4())
    payload = {"request_id": id}
    requests.post(vakuumsensor_url+"/trigger_measurement", json=payload)
    while requests.get(vakuumsensor_url+"/measurements/" + id).json()["state"] != "measured":
        time.sleep(2)
    result = requests.get(vakuumsensor_url+"/measurements/" + id).json()["result"]
    requests.delete(vakuumsensor_url+"/measurements/" + id)
    return result


class SensorService(analyzer_alpha_pb2_grpc.SensorVoidEnergyServerServicer):
    def read_sensor_data(self, request, context):
        print("Analyzer fragt Sensordaten an...")
        result = get_measure_data()
        print("result: ", result)
        return analyzer_alpha_pb2.SensorData(hexdata=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    analyzer_alpha_pb2_grpc.add_SensorVoidEnergyServerServicer_to_server(SensorService(), server)
    server.add_insecure_port("[::]:2102")
    server.start()
    print("SensorVoidEnergyServer läuft auf Port 2102")
    server.wait_for_termination()


serve()