#!/usr/bin/env python
# coding=utf-8

import argparse
import utils
import os.path
import fkchecker


def main():
    parser = get_arg_parser()
    args = parser.parse_args()

    endpoint = utils.format_endpoint(args.endpoint[0])
    options = None

    if args.datafile is not None:
        if os.path.exists(args.datafile):
            options = utils.load_json(args.datafile)
    else:
        fkjson_path = os.path.dirname(os.path.abspath(__file__)) + '/fkdata.json'
        if os.path.exists(fkjson_path):
            options = utils.load_json(fkjson_path)

    if options is None:
        print '''
        fkdata.json file needed...
        '''
    else:
        fk_checker = fkchecker.FkChecker(endpoint, options)
        fk_checker.execute()

        print 'Total Frames Received: ' + str(fk_checker.get_recv_frames)
        print 'Total Asserts: ' + str(fk_checker.get_asserts)
        print 'Total of validation executed: ' + str(fk_checker.get_validations_runned)
        print 'Assert frame rate: ' + str(fk_checker.get_assert_rate) + ' %'


def get_arg_parser():
    parser = argparse.ArgumentParser(description='FKWebsocketChecker')
    parser.add_argument('endpoint', nargs='+', help='The endpoint that should be checked.')
    parser.add_argument('-f', '--datafile', help='Json file to load check rules.')
    parser.add_argument('--version', action='version', version='%(prog)s ')
    return parser


if __name__ == "__main__":
    main()
