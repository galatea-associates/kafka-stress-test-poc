#!/bin/bash

number_tests=8
prices_procs=(1 2 4 8 16 23 64 128)
prices_data_procs=(1 1 1 1 1 1 1 1)

positions_procs=(1 1 2 4 8 16 23 64)
positions_data_procs=(1 1 1 1 1 1 1 1)

cp src/DataConfiguration_skele.py src/DataConfiguration.py

for (( i=0; i<${number_tests}; i++ ));
do

    # Setup configuration options
    cp src/DataConfiguration_skele.py src/DataConfiguration.py
    sed -i -e "s/%prices_procs%/${prices_procs[$i]}/g" src/DataConfiguration.py
    sed -i -e "s/%prices_data_procs%/${prices_data_procs[$i]}/g" src/DataConfiguration.py

    sed -i -e "s/%positions_procs%/${positions_procs[$i]}/g" src/DataConfiguration.py
    sed -i -e "s/%positions_data_procs%/${positions_data_procs[$i]}/g" src/DataConfiguration.py

    sed -i -e "s/%inst-ref_procs%/1/g" src/DataConfiguration.py
    sed -i -e "s/%inst-ref_data_procs%/1/g" src/DataConfiguration.py

    # Run test
    python3 src/SimpleProducer.py --serverIP=$1 --stopTime=300

    mkdir -p results/${i}
    mv out/output* results/${i}

done


