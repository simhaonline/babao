"""Argv parsing"""

import argparse

import babao.commands as cmd


def parseArgv(args):
    """Parse argv ´args´"""

    parser = argparse.ArgumentParser(
        description="A bitcoin trading machine.",
        epilog="Run 'babao <command> --help' for detailed help."
    )
    parser.add_argument(
        "-g", "--graph",
        help="show a chart (matplotlib)",
        action="store_true"
    )
    parser.add_argument(
        "-f", "--fuck-it",
        help="stop bitching about existing lockfile",
        dest="fuckit",
        action="store_true"
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v", "--verbose",
        help="increase output verbosity",
        action="count",
        default=1
    )
    group.add_argument(
        "-q", "--quiet",
        help="stfu damn bot",
        action="store_true"
    )

    subparsers = parser.add_subparsers(
        title="commands",
        metavar="<command> [<args>]"
    )

    parser_d = subparsers.add_parser(
        "dry-run",
        aliases="d",
        help="real-time bot simulation",
        description="real-time bot simulation",
    )
    parser_d.set_defaults(func=cmd.dryRun)

    parser_w = subparsers.add_parser(
        "wet-run",
        aliases="w",
        help="real-time bot with real-money!",
        description="real-time bot with real-money!",
    )
    parser_w.set_defaults(func=cmd.wetRun)

    parser_t = subparsers.add_parser(
        "training",
        aliases="t",
        help="train model(s)",
        description="train model(s)",
    )
    parser_t.set_defaults(func=cmd.train)

    parser_b = subparsers.add_parser(
        "backtest",
        aliases="b",
        help="backtest previously trained model(s)",
        description="backtest previously trained model(s)",
    )
    parser_b.set_defaults(func=cmd.backtest)

    parser_f = subparsers.add_parser(
        "fetch",
        aliases="f",
        help="fetch raw trade data since the beginning of times",
        description="fetch raw trade data since the beginning of times",
    )
    # parser_f.add_argument('TIMESTAMP', type=int, default=0, help="start date")
    parser_f.set_defaults(func=cmd.fetch)

    args = parser.parse_args(args=args)

    try:
        args.func
    except AttributeError:
        parser.print_help()
        parser.exit()

    return args
