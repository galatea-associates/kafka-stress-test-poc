import atexit
import time

import avro.schema
from avro.io import DatumWriter
from kafka import KafkaProducer

import csv
import io
import json
from Counter import Counter
from DataConfiguration import configuration
from argparse import ArgumentParser
from multiprocessing import Manager, Process, Queue
from DataGenerator import DataGenerator

class Producer(object):
    def __init__(self, init_val=0, limit_val=0):
        self.sent_counter = Counter(init_val=init_val, limit_val=limit_val)
        self.received_counter = Counter(init_val=init_val, limit_val=limit_val)


def serialize_val(val, serializer, schema=None):
    if serializer == "Avro":
        writer = DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(val, encoder)
        return bytes_writer.getvalue()
    elif serializer == "JSON":
        return json.dumps(val)
    else:
        return val


def process_val(val, args=None):
    if callable(val):
        return process_val(val())
    elif isinstance(val, DataGenerator):
        return process_val(val.run(args))
    else:
        return val


def send(server_args, producer_counters, topic, shared_data_queue, wait_for_response, avro_schema, serializer):
    producer = KafkaProducer(bootstrap_servers=[str(server_args.ip) +":"+ str(server_args.port)])
    atexit.register(cleanup_producer, producer=producer)
    if avro_schema:
        schema = avro.schema.Parse(open(avro_schema).read())
    else:
        schema = None    
    while True:
        while producer_counters.sent_counter.check_value_and_increment():
            val = shared_data_queue.get()
            if wait_for_response:
                producer.send(topic, serialize_val(val, serializer, schema)).add_callback(producer_counters.received_counter.increment)
            else:
                producer.send(topic, val)


def reset_every_second(producer_counters, topic, time_interval, prev_time, shared_dict):
    while True:
        if time.time() - prev_time >= time_interval:
            counter_size = producer_counters.received_counter.value()
            producer_counters.received_counter.reset()
            producer_counters.sent_counter.reset()
            shared_dict[topic].append(int(counter_size))
            prev_time = time.time()


def data_pipe_producer(shared_data_queue, data_generator, max_queue_size, data_args):
    while True:
        if shared_data_queue.qsize() < max_queue_size:
            shared_data_queue.put(process_val(data_generator, data_args))

def start_sending(server_args, producer_counters, topic, data_generator, numb_prod_procs=1, numb_data_procs=1,
                  time_interval=1, wait_for_response=True, avro_schema=None, serializer=None, max_data_pipe_size=100,
                  data_args=None):
    shared_dict[topic] = manager.list() 
    shared_data_queue = Queue()

    procs = [Process(target=send, args=(server_args, producer_counters, topic, shared_data_queue, wait_for_response, avro_schema, serializer)) for i in range(numb_prod_procs)]
    timer_proc = Process(target=reset_every_second, args=(producer_counters, topic, time_interval, time.time(), shared_dict))
    data_gen_procs = [Process(target=data_pipe_producer, args=(shared_data_queue, data_generator, max_data_pipe_size, data_args)) for i in range(numb_data_procs)]

    procs.append(timer_proc)
    procs+=data_gen_procs
    for p in procs: p.start()
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
    producer_list = []

    for topic in config:
        producer_counters=Producer(init_val=config[topic]["Counter"]["init_val"], limit_val=config[topic]["Counter"]["limit_val"])
        producer_list.append(producer_counters)
        procs = start_sending(server_args=server_args, 
                                producer_counters=producer_counters, 
                                topic=topic, 
                                data_generator=config[topic]["Data"], 
                                numb_prod_procs=config[topic]["Number of Processes"], 
                                numb_data_procs=config[topic]["Number of Data Generation Processes"], 
                                time_interval=config[topic]["Time Interval"], 
                                avro_schema=config[topic]["Avro Schema"],
                                serializer=config[topic]["Serializer"],
                                max_data_pipe_size=config[topic]["Data Queue Max Size"],
                                data_args=config[topic]['Data Args'])
        topics_procs.append(procs)

    return topics_procs, producer_list

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--serverIP", dest="ip",
                        help="Kafka server address", required=True)
    parser.add_argument("-p", "--serverPort", dest="port",
                        help="Kafka server port", default=9092 )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    global manager, shared_dict

    server_args = parse_args()

    manager =  Manager()
    shared_dict = manager.dict()    

    topics_procs, producer_list = process_data_config(configuration, server_args)

    atexit.register(cleanup, config=configuration, topics_procs=topics_procs)
    input("Press Enter to exit...")

