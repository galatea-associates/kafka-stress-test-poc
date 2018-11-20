from DataGenerator import generate_inst_ref_entity
from DataGenerator import generate_price_entity
from DataGenerator import generate_position_entity

# This file will contrain the core configuration for running the consumer and producer.
# It will also contain the functions needed to generate data for the different topics.

configuration = {
    "prices": {
        "Counter": {
            "init_val" : 0,
            "limit_val" : 40000
        },
        "Serialization": {
            "Type": "Avro",
            "Schema": "prices.avsc",
        },
        "Data" : {
            "Generator Type": "Function",
            "Generator" : generate_price_entity
        },
        "Number of Processes" : 11,
        "Time Interval" : 1.0      
    },
    "positions": {
        "Counter": {
            "init_val" : 0,
            "limit_val" : 20000
        },
        "Serialization": {
            "Type": "Avro",
            "Schema": "positions.avsc",
        },
        "Data" : {
            "Generator Type": "Function",
            "Generator" : generate_position_entity
        },
        "Number of Processes" : 4,
        "Time Interval" : 1.0      
    },
    "instrument_reference_data": {
        "Counter": {
            "init_val" : 0,
            "limit_val" : 100
        },
        "Serialization": {
            "Type": "Avro",
            "Schema": "instrument_reference_data.avsc",
        },
        "Data" : {
            "Generator Type": "Function",
            "Generator" : generate_inst_ref_entity
        },
        "Number of Processes" : 1,
        "Time Interval" : 60.0      
    },
}