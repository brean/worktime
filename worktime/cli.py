#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

"""worktime command line tool."""

import os
import argparse
import argcomplete
import logging
from .worktime import login, print_work_times

CONFIG_FORMATTER = '%(asctime)s %(name)s[%(levelname)s] %(message)s'
logger = logging.getLogger(__name__)

def setup_logging():
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level)
    logging.basicConfig(level=log_level, format=CONFIG_FORMATTER)


def main():
    logger = setup_logging()
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        'server', help='URI to your caldav Server. E.g. '
        'http://owncloud-server.com/remote.php/dav/')
    parser.add_argument(
        '-s', '--secret_file', help='Path to your secret-file.', 
        default='secrets.txt')
    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    client = login(server=args.server, secret_file=args.secret_file)
    print_work_times(client=client)


if __name__ == '__main__':
    main()