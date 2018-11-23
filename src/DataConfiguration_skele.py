from CSVReader import CSVReader
# This file will contrain the core configuration
# for running the consumer and producer.

# It will also contain the functions needed to
# generate data for the different topics.
#

configuration = {
    "prices": {
        "Counter": {
            "Initial Value": 0,
            "Limit Value": 40000
        },
        "Avro Schema - Keys": "src/prices-keys.avsc",
        "Avro Schema - Values": "src/prices-values.avsc",
        "Serializer": "Avro",
        "Data": CSVReader(),
        "Data Args": {
            'File': 'src/out/prices.csv',
            'Format': 'CSV',
            'Chunk Size': 10,
            'Loop on end': True
        },
        "Data Queue Max Size": 40000,
        "Keys": ["inst_id"],
        "Load data first": True,
        "Number of Processes": %prices_procs%,
        "Number of Data Generation Processes": %prices_data_procs%,
        "Time Interval": 1.0
    },
    "positions": {
        "Counter": {
            "Initial Value": 0,
            "Limit Value": 20000
        },
        "Avro Schema - Keys": "src/positions-keys.avsc",
        "Avro Schema - Values": "src/positions-values.avsc",
        "Serializer": "Avro",
        "Data": CSVReader(),
        "Data Args": {
            'File': 'src/out/positions.csv',
            'Format': 'CSV',
            'Chunk Size': 10,
            'Loop on end': True
        },
        "Data Queue Max Size": 20000,
        "Keys": ["type", "knowledge_date", 
                 "effective_date", "account", "inst_id", "purpose"],
        "Load data first": True,
        "Number of Processes": %positions_procs%,
        "Number of Data Generation Processes": %positions_data_procs%,
        "Time Interval": 1.0
    },
    "instrument_reference_data": {
        "Counter": {
            "Initial Value": 0,
            "Limit Value": 100
        },
        "Avro Schema - Keys": "src/instrument_reference_data-keys.avsc",
        "Avro Schema - Values": "src/instrument_reference_data-values.avsc",
        "Serializer": "Avro",
        "Data": CSVReader(),
        "Data Args": {
            'File': 'src/out/inst-ref.csv',
            'Format': 'CSV',
            'Chunk Size': 10,
            'Loop on end': True
        },
        "Data Queue Max Size": 200,
        "Keys": ["inst_id"],
        "Load data first": True,
        "Number of Processes": %inst-ref_procs%,
        "Number of Data Generation Processes": %inst-ref_data_procs%,
        "Time Interval": 60.0
    },
}
