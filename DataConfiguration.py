# This file will contrain the core configuration for running the consumer and producer.
# It will also contain the functions needed to generate data for the different topics.

{
    "prices": {
        "Counter": {
            "init_val" : 0,
            "limit_val" : 40000
        },
        "Value" : b'1.0', #TODO: Change this to some function call  
        "Number of Processes" : 11,
        "Time Interval" : 1.0      
    },
    "positions": {
        "Counter": {
            "init_val" : 0,
            "limit_val" : 20000
        },
        "Value" : b'This is the position data', #TODO: Change this to some function call  
        "Number of Processes" : 4,
        "Time Interval" : 1.0      
    },
    "instrument_reference_data": {
        "Counter": {
            "init_val" : 0,
            "limit_val" : 100
        },
        "Value" : b'InstRef', #TODO: Change this to some function call  
        "Number of Processes" : 1,
        "Time Interval" : 60.0      
    },
}