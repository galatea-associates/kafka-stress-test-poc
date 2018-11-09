from DataGenerator import DataGenerator

# This file will contrain the core configuration for running the consumer and producer.
# It will also contain the functions needed to generate data for the different topics.

configuration = {
    "prices": {
        "Counter": {
            "Initial Value" : 0,
            "Limit Value" : 40000
        },
        "Avro Schema": "prices.avsc",
        "Serializer": "Avro",
        "Data" : DataGenerator.generate_price_entity,
        "Data Queue Max Size": 40,
        "Number of Processes" : 11,
        "Number of Data Generation Processes": 1,
        "Time Interval" : 1.0      
    },
    "positions": {
        "Counter": {
            "Initial Value" : 0,
            "Limit Value" : 20000
        },
        "Avro Schema": "positions.avsc",
        "Serializer": "Avro",
        "Data" : DataGenerator.generate_position_entity,
        "Data Queue Max Size": 20,
        "Number of Processes" : 4,
        "Number of Data Generation Processes": 1,
        "Time Interval" : 1.0      
    },
    "instrument_reference_data": {
        "Counter": {
            "Initial Value" : 0,
            "Limit Value" : 100
        },
        "Avro Schema": "instrument_reference_data.avsc",
        "Serializer": "Avro",
        "Data" : DataGenerator.generate_inst_ref_entity,
        "Data Queue Max Size": 5,
        "Number of Processes" : 1,
        "Number of Data Generation Processes": 1,
        "Time Interval" : 60.0      
    },
}