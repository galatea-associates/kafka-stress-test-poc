import atexit
import time

import avro.schema
import avro.io

from kafka import KafkaConsumer

import csv
import io
from Counter import Counter
from DataConfiguration import configuration
from argparse import ArgumentParser
from multiprocessing import Manager, Process



def close_consumer(consumer):
    consumer.close()


def receive(server_args, counter, topic, avro_schema):
    consumer = get_consumer(server_args, topic)
    atexit.register(close_consumer, consumer)
    if avro_schema:
        schema = avro.schema.Parse(open(avro_schema).read())
    for msg in consumer:
        if avro_schema:
            bytes_reader = io.BytesIO(msg.value)
            decoder = avro.io.BinaryDecoder(bytes_reader)
            reader = avro.io.DatumReader(schema)
            msg_data = reader.read(decoder)
        #TODO: Find out what data type was sent to know how to de-seralize it.
        counter.increment()

def get_consumer(server_args, topic):
    return KafkaConsumer(topic, bootstrap_servers=[str(server_args.ip) +":"+ str(server_args.port)])

def count_msgs_every_second(counter, topic, time_interval, prev_time, shared_dict):
    while True:
        if time.time() - prev_time >= time_interval:
            counter_size = counter.value()
            counter.reset()
            #print("Topic " + topic + " recieved " + str(counter_size) + " messages!")
            shared_dict[topic].append(int(counter_size))
            prev_time = time.time()

def start_receiving(server_args, topic, time_interval, numb_procs, avro_schema=None):
    counter = Counter(0)
    shared_dict[topic] = manager.list()
    procs = [Process(target=receive, args=(server_args, counter, topic, avro_schema)) for i in range(numb_procs)]
    for p in procs: p.start()
    timer_proc = Process(target=count_msgs_every_second, args=(counter, topic, time_interval, time.time(), shared_dict))
    timer_proc.start()
    procs.append(timer_proc)
    return procs

def cleanup_processes(procs):
    for p in procs: p.terminate()

def produce_output(dict_key, output_time):
    if len(shared_dict[dict_key]) == 0:
        return
    print(dict_key + " - Mean: " + str(sum(shared_dict[dict_key]) / len(shared_dict[dict_key])) + " Max: " + str(max(shared_dict[dict_key])) + " Min: " + str(min(shared_dict[dict_key])) ) 
    with open("output-recieve-" + str(int(output_time)) + ".csv", 'a', newline='') as output_file:
        wr = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        wr.writerow(shared_dict[dict_key])

def cleanup(topics_procs):
    for procs in topics_procs:
        cleanup_processes(procs)
    output_time = time.time()
    produce_output(dict_key="prices", output_time=output_time)
    produce_output(dict_key="positions", output_time=output_time)
    produce_output(dict_key="instrument_reference_data", output_time=output_time)


def process_data_config(config, server_args):

    topics_procs = []

    for topic in config:
        procs = start_receiving(server_args=server_args, topic=topic, numb_procs=config[topic]["Number of Processes"], time_interval=config[topic]["Time Interval"], avro_schema=config[topic]["Avro Schema"])
        topics_procs.append(procs)

    return topics_procs

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

    topics_procs = process_data_config(configuration, server_args)

    atexit.register(cleanup, topics_procs=topics_procs)
    input("Press Enter to exit...")