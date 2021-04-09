#!/usr/local/bin/python3.8
# -*- coding: utf-8 -*-

import argparse
import sys
import pathlib

import ippcode_interpreter as ipp


def argumentParse():
    """ Parse the arguments """
    parser = argparse.ArgumentParser(
        add_help=False,
        prog="interpret",
        description='IPPCode21 Interpret, Author: Ondřej Sloup (xsloup02)'
    )
    parser.add_argument('-s', '--source', type=pathlib.Path)
    parser.add_argument('-i', '--input', type=pathlib.Path)
    parser.add_argument('-h', '--help', action='store_true')

    try:
        args = parser.parse_args()
    except SystemExit:
        raise ipp.exception.ArgumentsNotValid()

    if (args.help and (args.input or args.source)):
        raise ipp.exception.ArgumentsInvalidCombination(
            "You can't use help with any other arguments")
    elif not (args.input or args.source or args.help):
        raise ipp.exception.ArgumentsInvalidCombination(
            "Please specify at least one argument")

    if args.help:
        print("""usage: interpret [-s SOURCE] [-i INPUT] [-h]\n\nIPPCode21 Interpret, Author: Ondřej Sloup (xsloup02)\n\noptional arguments:
  -s SOURCE, --source SOURCE
                        File with XML source code
  -i INPUT, --input INPUT
                        File with inputs for interpration of source code
  -h, --help            This messages""")
        sys.exit(ipp.exception.ErrorCodes.SUCCESS)

    if args.input is not None and not args.input.is_file():
        raise ipp.exception.FileNotFound()

    if args.source is not None and not args.source.is_file():
        raise ipp.exception.FileNotFound()
    return args


def main(args):
    """ Launcher for IPPCode package """
    ipp.ippcode.IPPCode21(args.source, args.input)


if __name__ == "__main__":
    args = argumentParse()
    main(args)
