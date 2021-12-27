import copy
import json
import os
import random
import sys
from argparse import ArgumentParser
from typing import List, Optional, Union

spec_templates = {
    "entity_value":
    '''
    {
      "type": "item",
      "properties": [
        {
          "property":"",
          "type": "entityid",
          "rank": "all",
          "value": ""
        }
      ]
    }
    ''',
    "nometa_noqual":
    '''
    {
    "version": "1",
    "entities": [
    ],
    "statements": [
        {
        "id": 0,
        "references": true,
        "simple": true,
        "rank": "all",
        "full": true,
        "qualifiers": false
        }
    ],
    "sitelinks": true,
    "descriptions": false,
    "aliases": false,
    "meta": false,
    "labels": false
    }
    '''
}


def genargs(prog: Optional[str] = None) -> ArgumentParser:
    parser = ArgumentParser(prog)
    parser.add_argument(
        "-o", "--output", help="Output file", default=os.getcwd()+os.sep+'rand_spec.json')
    parser.add_argument("-n", "--number",
                        help="Determines how many items will be in the specification file.", type=int)
    return parser


def main(argv: Optional[Union[str, List[str]]] = None, prog: Optional[str] = None) -> int:
    if isinstance(argv, str):
        argv = argv.split()
    opts = genargs(prog).parse_args(argv if argv is not None else sys.argv[1:])
    print("WARNING: bennofs wdumper is not supporting this script's output specs. You need to compile current repo.")
    spec = json.loads(spec_templates["nometa_noqual"])
    random_ids = random.sample(range(1,110272953), opts.number)
    
    for id in random_ids:
        new_entity_val = {"type": "item","properties": [{'type': 'entityid','rank': 'all','value': 'Q'+str(id),'property': ''}]}
        spec['entities'].append(new_entity_val)
    
    print('Writing {0} random QIDs to the config file: {1}'.format(opts.number,opts.output))
    with open(opts.output, 'w') as outfile:
        json.dump(spec, outfile, indent=3)
    print('DONE.')
    return 0



if __name__ == '__main__':
    main(sys.argv[1:])
