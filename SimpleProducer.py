import atexit
import csv
import time
import json
import io
import avro.schema
from avro.io import DatumWriter
from argparse import ArgumentParser
from Counter import Counter
from kafka import KafkaProducer
from multiprocessing import Manager, Process

from DataConfiguration import configuration

def process_val(val, schema=None, is_avro=False):
    if schema:
        writer = DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(process_val(val, is_avro=True), encoder)
        return bytes_writer.getvalue()
    if isinstance(val, bytes):
        return val
    elif isinstance(val, str):
        return val.encode()
    elif callable(val):
        return process_val(val(), is_avro=is_avro)
    elif (not is_avro) and isinstance(val, dict):
        return json.dumps(val)
    elif is_avro:
        return val
    else:
        return b''

def send(server_args, counter, topic, val, wait_for_response, avro_schema):
    producer = KafkaProducer(bootstrap_servers=[str(server_args.ip) +":"+ str(server_args.port)])
    atexit.register(cleanup_producer, producer=producer)
    if avro_schema:
        schema = avro.schema.Parse(open(avro_schema).read())
    else:
        schema = None    
    while True:
        while counter.check_value_and_increment():
            if wait_for_response:
                future = producer.send(topic, process_val(val, schema))
                result = future.get(timeout=60)
            else:
                producer.send(topic, val)


def reset_every_second(counter, topic, time_interval, prev_time, shared_dict):
    while True:
        if time.time() - prev_time >= time_interval:
            counter_size = counter.value()
            counter.reset()
            #print("Topic " + topic + " sent " + str(counter_size) + " messages!")
            shared_dict[topic].append(int(counter_size))
            prev_time = time.time()

def start_sending(server_args, counter, topic, val, numb_procs, time_interval, wait_for_response=True, avro_schema=None):
    shared_dict[topic] = manager.list() 
    procs = [Process(target=send, args=(server_args, counter, topic, val, wait_for_response, avro_schema)) for i in range(numb_procs)]
    for p in procs: p.start()
    timer_proc = Process(target=reset_every_second, args=(counter, topic, time_interval, time.time(), shared_dict))
    timer_proc.start()
    procs.append(timer_proc)
    return procs

def cleanup_processes(procs):
    for p in procs: p.terminate()

def cleanup_producer(producer):
    producer.close()

def produce_output(dict_key, output_time):
    if len(shared_dict[dict_key]) == 0:
        return
    print(dict_key + " - Mean: " + str(sum(shared_dict[dict_key]) / len(shared_dict[dict_key])) + " Max: " + str(max(shared_dict[dict_key])) + " Min: " + str(min(shared_dict[dict_key])) ) 
    with open("output-send-" + str(int(output_time)) + ".csv", 'a', newline='') as output_file:
        wr = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        wr.writerow(shared_dict[dict_key])

def cleanup(config, topics_procs):
    for procs in topics_procs:
        cleanup_processes(procs)
    output_time = time.time()
    for topic in config:
        produce_output(dict_key=topic, output_time=output_time)
 
def process_data_config(config, server_args):

    topics_procs = []
    counter_list = []

    for topic in config:
        new_counter = Counter(init_val=config[topic]["Counter"]["init_val"], limit_val=config[topic]["Counter"]["limit_val"])
        counter_list.append(new_counter)
        procs = start_sending(server_args=server_args, counter=new_counter, topic=topic, val=config[topic]["Value"], numb_procs=config[topic]["Number of Processes"], time_interval=config[topic]["Time Interval"], avro_schema=config[topic]["Avro Schema"])
        topics_procs.append(procs)

    return topics_procs, counter_list

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--serverIP", dest="ip",
                        help="Kafka server address", required=True)
    parser.add_argument("-p", "--serverPort", dest="port",
                        help="Kafka server port", default=9092 )

    args = parser.parse_args()
    return args


def run():
    global manager, shared_dict

    server_args = parse_args()

    manager =  Manager()
    shared_dict = manager.dict()    

    topics_procs, counter_list = process_data_config(configuration, server_args)

    atexit.register(cleanup, config=configuration, topics_procs=topics_procs)
    input("Press Enter to exit...")

if __name__ == '__main__':
    run()

