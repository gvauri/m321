import pika
import json
import travel as t


def scanner(handle_station):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="10.255.255.254", port=2014))
    channel = connection.channel()
    channel.exchange_declare(exchange='scanner/detected_objects', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='scanner/detected_objects', queue=queue_name)
    for method_frame, properties, body in channel.consume(queue=queue_name, auto_ack=True):
        for station in json.loads(body.decode('utf-8')):
            handle_station(station)

