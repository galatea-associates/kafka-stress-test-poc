import atexit
import time

import avro.schema
import avro.io

from kafka import KafkaConsumer

import csv
import io
import json
import statistics
from Counter import Counter
from DataConfiguration import configuration
from argparse import ArgumentParser
from multiprocessing import Manager, Process


def close_consumer(consumer):
    consumer.close()


def deserialize_msg(msg, serializer, schema=None):
    if serializer == "Avro":
        bytes_reader = io.BytesIO(msg.value)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(schema)
        msg_data = reader.read(decoder)
        return_val = msg_data
    elif serializer == "JSON":
        return_val = json.loads(msg)
    else:
        return_val = msg
    return return_val


def receive(server_args, counter, topic, avro_schema, serializer):
    consumer = get_consumer(server_args, topic)
    atexit.register(close_consumer, consumer)
    if avro_schema:
        schema = avro.schema.Parse(open(avro_schema).read())
    else:
        schema = None
    for msg in consumer:
        deserialize_msg(msg, serializer, schema)
        counter.increment()


def get_consumer(server_args, topic):
    server_addr = str(server_args.ip) + ":" + str(server_args.port)
    return KafkaConsumer(topic, bootstrap_servers=[server_addr])


def count_msgs_every_second(counter, topic, time_interval,
                            prev_time, shared_dict):
    while True:
        if time.time() - prev_time >= time_interval:
            counter_size = counter.value()
            counter.reset()
            shared_dict[topic].append(int(counter_size))
            prev_time = time.time()


def start_receiving(server_args, topic, time_interval, numb_procs,
                    avro_schema=None, serializer=None):
    counter = Counter(0)
    shared_dict[topic] = manager.list()

    procs = [Process(target=receive,
                     args=(server_args,
                           counter,
                           topic,
                           avro_schema,
                           serializer)) for i in range(numb_procs)]

    timer_proc = Process(target=count_msgs_every_second,
                         args=(counter,
                               topic,
                               time_interval,
                               time.time(),
                               shared_dict))

    procs.append(timer_proc)

    for p in procs:
        p.start()

    return procs


def cleanup_processes(procs):
    for p in procs:
        p.terminate()


def print_data_results(keys, dict_key):
    print(dict_key + ":")
    for key in keys:
        print(key + " -", end=' ')
        length = sum(1 for _ in (item[key] for item in shared_dict[dict_key]))
        print("Mean: " + str(sum(item[key] for item in shared_dict[dict_key]) / length), end=' ')
        print("Max: " + str(max(item[key] for item in shared_dict[dict_key])), end=' ')
        print("Min: " + str(min(item[key] for item in shared_dict[dict_key])), end=' ')
        if length > 1:
            print("Standard Deviation: " + str(statistics.stdev(item[key] for item in shared_dict[dict_key])))
    print()


def produce_output(dict_key, output_time):
    if not shared_dict[dict_key]:
        return
    keys = shared_dict[dict_key][0].keys()
    print_data_results(keys, dict_key)
    with open("out/output-recieve-" + str(int(output_time)) + ".csv",
              'a', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(shared_dict[dict_key])


def cleanup(config=None, topics_procs=None):
    for procs in topics_procs:
        cleanup_processes(procs)
    output_time = time.time()
    for topic in config:
        produce_output(dict_key=topic, output_time=output_time)


def process_data_config(config, server_args):

    topics_procs = []

    for topic in config:
        procs = start_receiving(server_args=server_args, 
                                topic=topic,         
                                numb_procs=config[topic]["Number of Processes"], 
                                time_interval=config[topic]["Time Interval"], 
                                avro_schema=config[topic]["Avro Schema - Values"],
                                serializer=config[topic]["Serializer"])
        topics_procs.append(procs)

    return topics_procs


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--serverIP", dest="ip",
                        help="Kafka server address", required=True)
    parser.add_argument("-p", "--serverPort", dest="port",
                        help="Kafka server port", default=9092)

    args = parser.parse_args()
    return args


def run():
    global manager, shared_dict

    server_args = parse_args()

    manager = Manager()
    shared_dict = manager.dict()    

    topics_procs = process_data_config(configuration, server_args)

    atexit.register(cleanup, config=configuration, topics_procs=topics_procs)
    input("Press Enter to exit...")


if __name__ == '__main__':
    run()
