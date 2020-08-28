#! /usr/bin/python3
import sys
import importlib
from .run import run
from .configuration import configuration_from_module

def validate_schema(filename):
    options = importlib.import_module(filename)

    config = configuration_from_module(options)
    return run(config)

if __name__ == '__main__':
    report = validate_schema(sys.argv[1])

    for line in report:
        print(line)
