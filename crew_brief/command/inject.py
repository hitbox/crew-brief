from crew_brief import configlib

def add_parser(subparsers):
    """
    Add sub-command parser for inject.
    """
    parser = subparsers.add_parser('inject', help=inject.__doc__)
    configlib.add_config_option(parser)
    parser.set_defaults(func=inject)

def inject(args):
    # Read Python config file.
    config = configlib.pyfile_config(args.config)

    inject_process = getattr(config, 'INJECT')
    subs = {}
    inject_process.run(subs)
