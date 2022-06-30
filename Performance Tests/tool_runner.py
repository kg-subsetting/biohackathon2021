import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Optional, Union


def genargs(prog: Optional[str] = None) -> ArgumentParser:
    parser = ArgumentParser(prog)
    parser.add_argument(
        "--tool", help="Tool to start the script", required=True)
    parser.add_argument(
        "--dump", help="Path to the Wikidata JSON file", required=True)
    return parser


def main(argv: Optional[Union[str, List[str]]] = None, prog: Optional[str] = None) -> int:
    if isinstance(argv, str):
        argv = argv.split()
    opts = genargs(prog).parse_args(argv if argv is not None else sys.argv[1:])

    opts.dump = Path(opts.dump)

    if opts.tool == 'wdumper':
        run_wdumper(opts.dump)
    elif opts.tool == 'wdf':
        run_wdf(opts.dump)
    elif opts.tool == 'wdsub':
        run_wdsub(opts.dump)
    elif opts.tool == 'kgtk':
        run_kgtk(opts.dump)
    else:
        print(
            'ERROR: Enter a valid tool. Valid tools are: "wdumper", "wdf", "wdsub", "kgtk"')
        return 1


def run_wdumper(dump: Path) -> int:
    print('Starting a new run of WDumper ...')


def run_wdf(dump: Path) -> int:
    print('Starting a new run of Wikibase Dump Filter ...')


def run_wdsub(dump: Path) -> int:
    print('Starting a new run of WDSub ...')


def run_kgtk(dump: Path) -> int:
    print('Starting a new run of KGTK ...')


if __name__ == '__main__':
    main(sys.argv[1:])
