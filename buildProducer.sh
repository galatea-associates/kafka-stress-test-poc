#!/bin/bash

cython3 -3 --embed -o SimpleProducer.c SimpleProducer.py
gcc -Os -I /usr/include/python3.6 SimpleProducer.c -lpython3.6m -o SimpleProducer

rm SimpleProducer.c
