import os, sys, json, requests, copy, time
from argparse import ArgumentParser
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Optional, Union, List

def genargs(prog: Optional[str] = None) -> ArgumentParser:
    parser = ArgumentParser(prog)
    parser.add_argument("input", help="Input WDumper specification file")
    parser.add_argument("output", help="Output WDumper specification file, enriched with the subclasses")
    parser.add_argument("-dp" , "--desiredproperty", help="Property that we want to include the subclasses of its values", default='P31')
    parser.add_argument("-iz" , "--ignorezero", help="Ignore subclasses that have no instances", action='store_true')
    return parser

def getResults(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url,user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def getResultsReq(endpoint_url, query):
    while True:
        response = requests.get(endpoint_url, headers = {'User-agent': 'your bot 0.1'}, params = {'format': 'json', 'query': query})
        if response.status_code == 429:
            print('Process should wait for {0}'.format(str(response.headers)))
            time.sleep(int(response.headers["Retry-After"]))
        elif response.status_code == 200:
            return response.json()

def removeCurrentProperty(prop_array:List, propert: object) -> List:
    for i in range(len(prop_array)):
        if prop_array[i]['property'] == propert['property'] and prop_array[i]['value'] == propert['value']:
            prop_array.pop(i)
            break
    return prop_array

def main(argv: Optional[Union[str, List[str]]] = None, prog: Optional[str] = None) -> int:
    if isinstance(argv, str):
        argv = argv.split()
    opts = genargs(prog).parse_args(argv if argv is not None else sys.argv[1:])
    if not os.path.exists(opts.input):
        print("ERROR - The input file does not exist.")
        return 1
    (outDir, outFilename) = os.path.split(opts.output)
    if not os.path.exists(outDir):
        print("ERROR - The output file does not exist.")
        return 1
    
    wikidataEndpoint = 'https://query.wikidata.org/sparql'
    queryTemplate = """
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT ?subtypeQIDs WHERE {{
        ?subtypeQIDs wdt:P279+ {0} .
    }}
    """
    queryTemplateIz = """
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT DISTINCT ?subtypeQIDs WHERE {{
        ?subtypeQIDs wdt:P279+ {0} .
        ?anotherItem wdt:{1} ?subtypeQIDs.
    }}
    """
    with open(opts.input) as datafile:
        data = json.load(datafile)
    outData=copy.deepcopy(data)
    #value_counts=["class,count"]
    added_subclasses=0 
    for entity in data['entities']:
        if entity['type']=='item':
            for propert in entity['properties']:
                if propert['property']==opts.desiredproperty and propert['type']=='entityid':
                    basePad = removeCurrentProperty(entity['properties'], propert)
                    if opts.ignorezero:
                        query=queryTemplateIz.format('wd:'+propert['value'],opts.desiredproperty)
                    else:
                        query=queryTemplate.format('wd:'+propert['value'])
                    print('Getting subclasses from Wikidata endpoint...')
                    results = getResultsReq(wikidataEndpoint, query)                    
                    print(len(results['results']['bindings']) , 'subclasses was fetched from Wikdiata')                    
                    for qid in results['results']['bindings']:
                        value=qid['subtypeQIDs']['value'].replace('http://www.wikidata.org/entity/','')
                        #time.sleep(0.2)                        
                        # if opts.ignorezero:
                        #     counts=getResultsReq(wikidataEndpoint, 'SELECT (COUNT(*) AS ?count) WHERE {{?item wdt:P31 wd:{0}}}'.format(value))
                        #     counts=counts['results']['bindings'][0]['count']['value']
                        #     value_counts.append(str(str(value) + ',' + str(counts))) 
                        #     if counts=='0' :                            
                        #         print('Subclass: ' + value + ' is not added because it had no instances in Wikidata')
                        #         continue
                        print('Adding subclass: ' + value + ' with all the same-level conditions')
                        added_subclasses += 1
                        tempPad={'type':'item','properties':[]}
                        tempPad['properties']+=basePad
                        tempPad['properties'].append({'type': 'entityid','rank': 'all','value': value,'property': opts.desiredproperty})
                        outData['entities'].append(tempPad)
    # if opts.ignorezero :
    #     value_counts_file=opts.input+'-instanceCounts.csv'
    #     with open(value_counts_file, 'w') as classCounts:
    #         for item in value_counts:
    #             classCounts.write("%s\n" % item)
    
    print('Writing new {0} subclasses to the new config file...'.format(added_subclasses))
    with open(opts.output, 'w') as outfile:
        json.dump(outData, outfile, indent=3)
    print('done.')
    return 0

if __name__ == '__main__':
    main(sys.argv[1:])
