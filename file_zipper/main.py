from . import argumentparser

def main(argv=None):
    """
    Parse command line and call command with arguments.
    """
    parser = argumentparser.parser()
    args = parser.parse_args(argv)
    command = args.command
    delattr(args, 'command')
    return command(parser, args)
