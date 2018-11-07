import atexit
import csv
import time

from Counter import Counter
from kafka import KafkaProducer

from multiprocessing import Manager, Process

from DataConfiguration import configuration

def process_val(val):
    if isinstance(val, bytes):
        return val
    elif isinstance(val, str):
        return val.encode()
    elif callable(val):
        return val()
    else:
        return b''

def send(counter, topic, val, wait_for_response):
    producer = KafkaProducer(bootstrap_servers=['ec2-3-8-1-159.eu-west-2.compute.amazonaws.com:9092'])
    atexit.register(cleanup_producer, producer=producer)
    while True:
        while counter.check_value_and_increment():
            if wait_for_response:
                future = producer.send(topic, process_val(val))
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

def start_sending(counter, topic, val, numb_procs, time_interval, wait_for_response=True):
    shared_dict[topic] = manager.list()
    procs = [Process(target=send, args=(counter, topic, val, wait_for_response)) for i in range(numb_procs)]
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
 
def process_data_config(config):

    topics_procs = []
    counter_list = []

    for topic in config:
        new_counter = Counter(init_val=config[topic]["Counter"]["init_val"], limit_val=config[topic]["Counter"]["limit_val"])
        counter_list.append(new_counter)
        procs = start_sending(counter=new_counter, topic=topic, val=config[topic]["Value"], numb_procs=config[topic]["Number of Processes"], time_interval=config[topic]["Time Interval"])
        topics_procs.append(procs)

    return topics_procs, counter_list

if __name__ == '__main__':
    global manager, shared_dict

    manager =  Manager()
    shared_dict = manager.dict()    

    topics_procs, counter_list = process_data_config(configuration)

    atexit.register(cleanup, config=configuration, topics_procs=topics_procs)
    input("Press Enter to exit...")

