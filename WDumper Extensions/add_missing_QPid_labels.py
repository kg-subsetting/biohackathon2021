import os, sys
from argparse import ArgumentParser
from typing import Optional, Union, List
from rdflib import Graph
from rdflib.namespace import RDF, RDFS
from rdflib import Namespace

def genargs(prog: Optional[str] = None) -> ArgumentParser:
    parser = ArgumentParser(prog)
    parser.add_argument("input", help="Input N-Triple file (WDumper decompressed output)")
    parser.add_argument("-o", "--output", help="Output destination file, enriched with the missing Q IDs", default='output.nt')
    #parser.add_argument("-iq" , "--includeQids", help="Search for missing Q IDs and add labels/descriptions of them to the input", action='store_true', default=)
    parser.add_argument("-ip" , "--includePids", help="Search for missing P IDs and add labels/descriptions of them too", action='store_true')
    return parser

def main(argv: Optional[Union[str, List[str]]] = None, prog: Optional[str] = None) -> int:
    if isinstance(argv, str):
        argv = argv.split()
    opts = genargs(prog).parse_args(argv if argv is not None else sys.argv[1:])
    if not os.path.exists(opts.input):
        print("ERROR - The input file does not exist.")
        return 1
    
    Schema=Namespace("http://schema.org/")
    Q_ctr=0
    P_ctr=0
    label_ctr=0
    desc_ctr=0
    g = Graph()
    
    print('Parsing the input file...')
    g.parse(opts.input, format='nt')
    
    print('Searching for missing Q IDs...')
    for o in g.objects():
        if "http://www.wikidata.org/entity/Q" in o :
            if len(list(g.objects(o, RDF.type))) == 0 :
                Q_ctr += 1
                print(o + ' is missing -> Fetching labels/descriptions from Wikidata... ')
                # obtain the item info from Wikidata
                missedItem=Graph().parse(o+'.ttl', format='ttl')
                for label in missedItem.objects(o,RDFS.label):
                    g.add((o,RDFS.label, label))
                    label_ctr+=1
                for desc in missedItem.objects(o,Schema.description):
                    g.add((o,Schema.description, desc))
                    desc_ctr+=1
    
    if opts.includePids:
        for p in g.predicates():
            if "http://www.wikidata.org/prop/direct/P" in p :
                if len(list(g.objects(p, RDFS.label))) == 0 :
                    P_ctr += 1
                    print(p + ' is missing -> Fetching labels/descriptions from Wikidata... ')
                    # obtain the item info from Wikidata
                    entityOfp=p.replace("http://www.wikidata.org/prop/direct/P","http://www.wikidata.org/entity/P")
                    missedItem=Graph().parse(entityOfp+'.ttl', format='ttl')
                    for label in missedItem.objects(entityOfp,RDFS.label):
                        g.add((p,RDFS.label, label))
                        label_ctr+=1
                    for desc in missedItem.objects(entityOfp,Schema.description):
                        g.add((p,Schema.description, desc))
                        desc_ctr+=1

    print('Writing to the output...')
    g.serialize(destination=opts.output, format='nt')
    print('Done: {0} missing Q IDs, {1} missing P IDs, {2} added labels, {3} added descriptions'.format(Q_ctr,P_ctr,label_ctr,desc_ctr))
    return 0
        
if __name__ == '__main__':
    main(sys.argv[1:])