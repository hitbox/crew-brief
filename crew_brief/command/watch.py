from crew_brief import configlib

def add_parser(subparsers):
    """
    Add sub-command parser for watch.
    """
    parser = subparsers.add_parser('watch', help=watch.__doc__)
    configlib.add_config_option(parser)
    parser.set_defaults(func=watch)

def watch(args):
    # Read Python config file.
    config = configlib.pyfile_config(args.config)

    watch = getattr(config, 'WATCH')
    subs = {}
    watch.run(subs)
