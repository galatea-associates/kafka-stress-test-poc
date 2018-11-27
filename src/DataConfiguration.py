from CSVReader import CSVReader
from ParallelCSVReader import ParallelCSVReader
# This file will contrain the core configuration for running the consumer and producer.
# It will also contain the functions needed to generate data for the different topics.

configuration = {
    "prices": {
        "Counter": {
            "Initial Value": 0,
            "Limit Value": 40000
        },
        "Avro Schema - Keys": "src/prices-keys.avsc",
        "Avro Schema - Values": "src/prices-values.avsc",
        "Serializer": "Avro",
        # "Data": ParallelCSVReader(),
        "Data": CSVReader(),
        "Data Args": {
            'File': 'out/prices.csv',
            'Format': 'CSV',
            'Chunk Size': 10,
            'Loop on end': True
        },
        "Data Queue Max Size": 40000,
        "Keys": ["inst_id"],
        "Load data first": True,
        "Number of Processes": 2,
        "Number of Data Generation Processes": 2,
        "Time Interval": 1.0      
    },
}
