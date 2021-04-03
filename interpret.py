#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from sys import exit
import pathlib
import logging

import ippcode_interpreter as ipp


def argumentParse():
    """ Parse the arguments """
    parser = argparse.ArgumentParser(add_help=False,
                                     prog="interpret", description='IPPCode21 Interpret, Author: Ondřej Sloup (xsloup02)')
    parser.add_argument('-s', '--source', type=pathlib.Path)
    parser.add_argument('-i', '--input', type=pathlib.Path)
    parser.add_argument('-h', '--help', action='store_true')

    try:
        args = parser.parse_args()
    except SystemExit:
        exit(ipp.exception.ErrorCodes.ERR_ARGUMENT_PARSE_COMBINATION.value)

    if (args.help and (args.input or args.source)):
        parser.error("You can't use help with any other arguments")
        exit(ipp.exception.ErrorCodes.ERR_ARGUMENT_PARSE_COMBINATION.value)
    elif not (args.input or args.source or args.help):
        parser.error('Please specify at least one argument')
        exit(ipp.exception.ErrorCodes.ERR_ARGUMENT_PARSE_COMBINATION.value)
    if args.help:
        print("""usage: interpret [-s SOURCE] [-i INPUT] [-h]\n\nIPPCode21 Interpret, Author: Ondřej Sloup (xsloup02)\n\noptional arguments:
  -s SOURCE, --source SOURCE
                        File with XML source code
  -i INPUT, --input INPUT
                        File with inputs for interpration of source code
  -h, --help            This messages""")
        exit(ErrorCodes.SUCCESS.value)

    if args.input is not None and not args.input.is_file():
        logging.error("Input file not found")
        exit(ipp.exception.ErrorCodes.ERR_OPENING_FILES.value)

    if args.source is not None and not args.source.is_file():
        logging.error("Source file not found")
        exit(ipp.exception.ErrorCodes.ERR_OPENING_FILES.value)
    return args

def setupLogging():

    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s:[%(asctime)s] - %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S')
    return

def main(args):
    """ Main program """

    ipp.ippcode.IPPCode21(args.source, args.input)

if __name__ == "__main__":
    setupLogging()
    args = argumentParse()
    main(args)
