#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from sys import exit
import pathlib
import xml.etree.ElementTree as ET

from classes import IPPCode20
from errorCodes import ErrorCodes

def argumentParse():
    parser = argparse.ArgumentParser(add_help=False,
                                     prog="interpret", description='IPPCode21 Interpret, Author: Ondřej Sloup (xsloup02)')
    parser.add_argument('-s', '--source', type=pathlib.Path)
    parser.add_argument('-i', '--input', type=pathlib.Path)
    parser.add_argument('-h', '--help', action='store_true')

    try:
        args = parser.parse_args()
    except SystemExit:
        exit(ErrorCodes.ERR_ARGUMENT_PARSE_COMBINATION.value)

    if (args.help and (args.input or args.source)):
        parser.error("You can't use help with any other arguments")
        exit(ErrorCodes.ERR_ARGUMENT_PARSE_COMBINATION.value)
    elif not (args.input or args.source or args.help):
        parser.error('Please specify at least one argument')
        exit(ErrorCodes.ERR_ARGUMENT_PARSE_COMBINATION.value)
    if args.help:
        print("""usage: interpret [-s SOURCE] [-i INPUT] [-h]\n\nIPPCode21 Interpret, Author: Ondřej Sloup (xsloup02)\n\noptional arguments:
  -s SOURCE, --source SOURCE
                        File with XML source code
  -i INPUT, --input INPUT
                        File with inputs for interpration of source code
  -h, --help            This messages""")
        ex(ErrorCodes.SUCCESS.value)


    if args.input is not None and not args.input.is_file():
            print("Input file not found")
            exit(ErrorCodes.ERR_OPENING_FILES.value)

    if args.source is not None and not args.source.is_file():
            print("Source file not found")
            exit(ErrorCodes.ERR_OPENING_FILES.value)
    return args

def main(args):
    """ Main program """

    input_file = "lalala"

    IPPCode20(args, input_file)

if __name__ == "__main__":
    args = argumentParse()
    main(args)


