from .argument_parser import argument_parser

parser = argument_parser()
args = parser.parse_args()
args.func(args)
