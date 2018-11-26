import atexit
import time

import cProfile

import avro.schema
from avro.io import DatumWriter
from kafka import KafkaProducer

import csv
import io
import json
from Counter import Counter
from DataConfiguration import configuration
from DataGenerator import DataGenerator
from argparse import ArgumentParser
from multiprocessing import Value, Manager, Process
from fmq import Queue
import queue
import os
import math
import statistics


class Producer():
    def __init__(self, init_val=0, limit_val=0, ready_start_prod=False):
        self.sent_counter = Counter(init_val=init_val, limit_val=limit_val)
        self.received_counter = Counter(init_val=init_val, limit_val=limit_val)
        self.ready_start_producing = Value('i', ready_start_prod)
        self.error_counter = Counter(init_val=init_val, limit_val=math.inf)
        self.end_topic = Value('i', False)

def serialize_val(val, serializer, schema=None):
    if serializer == "Avro":
        writer = DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(val, encoder)
        return_val = bytes_writer.getvalue()
    elif serializer == "JSON":
        return_val = json.dumps(val)
    else:
        return_val = val
    return return_val


def process_val(val, args=None):
    if callable(val):
        return_val = process_val(val())
    elif isinstance(val, DataGenerator):
        return_val = process_val(val.run(args))
    else:
        return_val = val
    return return_val

def send(server_args, producer_counters, topic, shared_data_queue,
         avro_schema_keys, avro_schema_values, serializer):
    server_addr = str(server_args.ip) + ":" + str(server_args.port)
    producer = KafkaProducer(bootstrap_servers=[server_addr])
    atexit.register(cleanup_producer, producer=producer)
    schema_keys = None
    schema_values = None

    if avro_schema_keys:
        schema_keys = avro.schema.Parse(open(avro_schema_keys).read())
    if avro_schema_values:
        schema_values = avro.schema.Parse(open(avro_schema_values).read())
        
    while not bool(producer_counters.ready_start_producing.value):
        pass
    while True:
        while producer_counters.sent_counter.check_value_and_increment():
            if bool(producer_counters.end_topic.value):
                return
            try:
                val = shared_data_queue.get_nowait()
            except queue.Empty:
                print(str(topic) + " - Queue is Empty. Now Quitting this topic.")
                producer_counters.end_topic.value = int(True)
                return
            if val is None:
                print(str(topic) + " - Value is returned as None. Now Quitting this topic.")
                producer_counters.end_topic.value = int(True)
                return
            producer.send(topic,
                          value=serialize_val(val["value"],
                                              serializer,
                                              schema_values),
                          key=serialize_val(val["key"],
                                            serializer,
                                            schema_keys)
                          ).add_callback(on_send_success,
                                         producer_counters).add_errback(on_send_error,
                                                                        producer_counters)


def on_send_success(producer_counters, _):
    producer_counters.received_counter.increment()


def on_send_error(producer_counters, _):
    producer_counters.error_counter.increment()


def reset_every_second(producer_counters, topic, time_interval, shared_dict, shared_data_queue, max_queue_size):
    while ((not bool(producer_counters.ready_start_producing.value)) and 
           (shared_data_queue.qsize() < max_queue_size)):
        time.sleep(1)
    producer_counters.ready_start_producing.value = int(True)
    print(topic + "- Ready to start sending")
    prev_time = time.time()
    while True:
        if bool(producer_counters.end_topic.value):
            return
        time_now = time.time()
        if time_now - prev_time >= time_interval: 
            time_diff = (time_now - prev_time)
            result = {
                "Sent Counter": time_interval * (producer_counters.sent_counter.value() / time_diff),
                "Received Counter": time_interval * (producer_counters.received_counter.value() / time_diff),
                "Error Counter": time_interval * (producer_counters.error_counter.value() / time_diff)
            }
            producer_counters.received_counter.reset()
            producer_counters.sent_counter.reset()
            producer_counters.error_counter.reset()
            shared_dict[topic].append(result)
            prev_time = time_now


def split_key_and_value(data, keys=None):
    keys_dict = {}
    values_dict = {}
    for key in keys:
        keys_dict[key] = data[key]

    value_keys = list(set(data.keys()).difference(keys))
    for value_key in value_keys:
        values_dict[value_key] = data[value_key]
        
    return {"key": keys_dict, "value": values_dict}


def data_pipe_producer(shared_data_queue, data_generator, max_queue_size, data_args, keys):
    while True:
        if shared_data_queue.qsize() < max_queue_size:
            data = process_val(data_generator, data_args)
            if data is None:
                # Means producer has finished sending
                shared_data_queue.put(data)
                break
            if isinstance(data, list):
                for item in data:
                    shared_data_queue.put(split_key_and_value(data=item,
                                                              keys=keys))
            else:
                shared_data_queue.put(split_key_and_value(data=data, keys=keys))
        else:
            break


def profile_senders(server_args, producer_counters, topic, shared_data_queue,
                    avro_schema_keys, avro_schema_values, serializer, i):
    cProfile.runctx(('send(server_args, producer_counters, topic, '
                     'shared_data_queue, avro_schema_keys, '
                     'avro_schema_values, serializer)'),
                    globals(),
                    locals(),
                    'senders-prof%d.prof' % i)

def profile_data_pipe_producer(shared_data_queue, data_generator,
                               max_queue_size, data_args, keys, i):
    cProfile.runctx(('data_pipe_producer(shared_data_queue, '
                     'data_generator, max_queue_size, '
                     'data_args, keys)'),
                    globals(),
                    locals(),
                    'data-prod-prof%d.prof' % i)

def start_sending(server_args, producer_counters, topic, data_generator, numb_prod_procs=1, numb_data_procs=1,
                  time_interval=1, avro_schema_keys=None, avro_schema_values=None, serializer=None, max_data_pipe_size=100,
                  data_args=None, keys=None):

    shared_dict[topic] = manager.list()
    shared_data_queue = Queue()

    procs = []

    data_gen_procs = [Process(target=profile_data_pipe_producer,
                              args=(shared_data_queue,
                                    data_generator,
                                    max_data_pipe_size,
                                    data_args,
                                    keys,
                                    i)) for i in range(numb_data_procs)]

    #data_gen_procs = [Process(target=data_pipe_producer,
    #                          args=(shared_data_queue,
    #                                data_generator,
    #                                max_data_pipe_size,
    #                                data_args,
    #                                keys)) for _ in range(numb_data_procs)]

    # producer_procs = [Process(target=profile_senders,
    #                          args=(server_args,
    #                                producer_counters,
    #                                topic,
    #                                shared_data_queue,
    #                                avro_schema_keys,
    #                                avro_schema_values,
    #                                serializer,
    #                                i)) for i in range(numb_prod_procs)]
    producer_procs = [Process(target=send,
                              args=(server_args,
                                    producer_counters,
                                    topic,
                                    shared_data_queue,
                                    avro_schema_keys,
                                    avro_schema_values,
                                    serializer)) for _ in range(numb_prod_procs)]

    timer_proc = Process(target=reset_every_second,
                         args=(producer_counters,
                               topic,
                               time_interval,
                               shared_dict,
                               shared_data_queue,
                               max_data_pipe_size))

    for p in data_gen_procs:
        p.start()

    # Sleep for a second to let the data generators have time to push some data into the queue
    time.sleep(5.0)
    procs += producer_procs
    procs.append(timer_proc)
    for p in procs: 
        p.start()
    procs += data_gen_procs
    return procs


def cleanup_processes(procs):
    for p in procs:
        p.terminate()


def cleanup_producer(producer):
    producer.close()


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
    output_directory = "out"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    keys = shared_dict[dict_key][0].keys()
    print_data_results(keys, dict_key)
   
    with open(output_directory + "/output-send-" + str(int(output_time)) + ".csv",
              'a',
              newline='') as output_file:
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
    producer_list = []

    for topic in config:

        producer_counters = Producer(init_val=config[topic]["Counter"]["Initial Value"],
                                     limit_val=config[topic]["Counter"]["Limit Value"],
                                     ready_start_prod=(not config[topic]['Load data first']))
        producer_list.append(producer_counters)

        procs = start_sending(server_args=server_args, 
                              producer_counters=producer_counters, 
                              topic=topic, 
                              data_generator=config[topic]["Data"], 
                              numb_prod_procs=config[topic]["Number of Processes"], 
                              numb_data_procs=config[topic]["Number of Data Generation Processes"], 
                              time_interval=config[topic]["Time Interval"], 
                              avro_schema_keys=config[topic]["Avro Schema - Keys"],
                              avro_schema_values=config[topic]["Avro Schema - Values"],
                              serializer=config[topic]["Serializer"],
                              max_data_pipe_size=config[topic]["Data Queue Max Size"],
                              data_args=config[topic]['Data Args'],
                              keys=config[topic]["Keys"])

        topics_procs.append(procs)

    return topics_procs, producer_list


def parse_args():
    parser = ArgumentParser()

    parser.add_argument("-i",
                        "--serverIP",
                        dest="ip",
                        help="Kafka server address",
                        required=True)

    parser.add_argument("-p",
                        "--serverPort",
                        dest="port",
                        help="Kafka server port",
                        default=9092)

    parser.add_argument("-s",
                        "--stopTime",
                        dest="stop",
                        help="Kafka server port",
                        default=None)

    args = parser.parse_args()
    return args


def run():
    global manager, shared_dict

    server_args = parse_args()

    manager = Manager()
    shared_dict = manager.dict()    

    topics_procs, _ = process_data_config(configuration,
                                          server_args)

    atexit.register(cleanup, config=configuration, topics_procs=topics_procs)

    print("Producer script started")
    if server_args.stop and server_args.stop.isdigit():
        time.sleep(int(server_args.stop))
    else:
        input("Press Enter to exit...")


if __name__ == '__main__':
    run()
