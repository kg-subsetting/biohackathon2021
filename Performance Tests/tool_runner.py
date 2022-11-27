import subprocess
import sys
from argparse import ArgumentParser
from datetime import datetime
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
    print('=================================')
    start_time = datetime.now()
    process = subprocess.Popen('./WDUMPER/wdumper/build/install/wdumper/bin/wdumper-cli {0} {1}'.format(str(dump), './gene_protein_disease_chemicals.json'), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    process.wait()
    end_time = datetime.now()
    run_time = end_time - start_time
    print('=================================')
    print('DONE WDumper, Exec time: {0}'.format(run_time.total_seconds()))
    with open('wdumper_run_'+datetime.today().strftime('%Y-%m-%d-%H:%M:%S')+'.txt', 'w') as file:
        file.write(str(run_time))
    


def run_wdf(dump: Path) -> int:
    print('Starting a new run of Wikibase Dump Filter ...')
    print('=================================')
    start_time = datetime.now()
    process = subprocess.Popen('cat {0} | gzip -d |  ./WDF/wikibase-dump-filter/node_modules/.bin/wikibase-dump-filter --claim P31:Q11173,Q12136,Q7187,Q8054 > ./wdf.ndjson'.format(str(dump)), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    process.wait()
    end_time = datetime.now()
    run_time = end_time - start_time
    print('=================================')
    print('DONE WDF, Exec time: {0}'.format(run_time.total_seconds()))
    with open('wdf_run_'+datetime.today().strftime('%Y-%m-%d-%H:%M:%S')+'.txt', 'w') as file:
        file.write(str(run_time))



def run_wdsub(dump: Path) -> int:
    print('Starting a new run of WDSub ...')
    print('=================================')
    start_time = datetime.now()
    process = subprocess.Popen('./WDSUB/wdsubroot-0.0.28/bin/wdsubroot dump -s ./gene_protein_disease_chemicals.shex -o ./wdsub_output.ttl.gz {0} --schemaFormat ShEXC --dumpMode WholeEntity --dumpFormat Turtle'.format(str(dump)), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    process.wait()
    end_time = datetime.now()
    run_time = end_time - start_time
    print('=================================')
    print('DONE WDSub, Exec time: {0}'.format(run_time.total_seconds()))
    with open('wdsub_run_'+datetime.today().strftime('%Y-%m-%d-%H:%M:%S')+'.txt', 'w') as file:
        file.write(str(run_time))




def run_kgtk(dump: Path) -> int:
    print('Starting a new run of KGTK ...')
    print('=================================')
    start_time = datetime.now()
    process = subprocess.Popen('kgtk --debug --timing --progress import-wikidata -i {0} --node nodefile.tsv --edge edgefile.tsv --qual qualfile.tsv --use-mgzip-for-input True --use-mgzip-for-output True --use-shm True --procs 6 --mapper-batch-size 5 --max-size-per-mapper-queue 3 --single-mapper-queue True --collect-results True --collect-seperately True --collector-batch-size 10 --collector-queue-per-proc-size 3 --progress-interval 500000 --fail-if-missing False'.format(str(dump)), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.wait()
    command = '''kgtk query --gc ./wikidata.sqlite3.db -i edgefile.tsv --match '(n1)-[:P31]->(class), (n1)-[p]->(n2)'  --where 'class IN ["Q11173","Q12136","Q7187","Q8054"]' --return 'n1, p, n2' > ./kgtk_output.tsv'''
    process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    process.wait()

    end_time = datetime.now()
    run_time = end_time - start_time
    print('=================================')
    print('DONE KGTK, Exec time: {0}'.format(run_time.total_seconds()))
    with open('kgtk_run_'+datetime.today().strftime('%Y-%m-%d-%H:%M:%S')+'.txt', 'w') as file:
        file.write(str(run_time))



if __name__ == '__main__':
    main(sys.argv[1:])
