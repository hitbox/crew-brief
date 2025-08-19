import argparse

def argument_parser():
    """
    Create scheduled tasks argument parser.
    """

    parser = argparse.ArgumentParser(
        description = 'Project specific Windows\' scheduled tasks commands.'
    )
    parser.add_argument(
        '--config',
        help = 'Python file for configuration specifying the scheduled tasks.',
    )

    return parser
