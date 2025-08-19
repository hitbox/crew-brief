import os

from .argument_parser import argument_parser

def main(argv=None):
    """
    Main entry point for command line. Parser command line options and call
    command with arguments.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)

    config = args.config
    if not config:
        config = os.env.get()
