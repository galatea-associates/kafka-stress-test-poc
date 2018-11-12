#!/bin/bash

cython3 -3 --embed -o SimpleConsumer.c SimpleConsumer.py
gcc -Os -I /usr/include/python3.6 SimpleConsumer.c -lpython3.6m -o SimpleConsumer

rm SimpleConsumer.c
