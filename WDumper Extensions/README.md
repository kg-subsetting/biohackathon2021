## WDumper Extensions

In this directory you can find some useful WDumper extensions. Extensions so far are:

### Add subclasses to WDumper specification file
Use `add_subclasses.py` script as follows to **enrich an existing WDumper spec file with subclasses**:
```
usage: add_subclasses.py [-h] [-dp DESIREDPROPERTY] [-iz] input output

positional arguments:
  input                 Input WDumper specification file
  output                Output WDumper specification file, enriched with the
                        subclasses

optional arguments:
  -h, --help            show this help message and exit
  -dp DESIREDPROPERTY, --desiredproperty DESIREDPROPERTY
                        Property that we want to include the subclasses of its
                        values
  -iz, --ignorezero     Ignore subclasses that have no instances
```
An example using the repo files will include subclasses of every `P31` valued filter that have at least one instance in Wikidata:
```
python ./add_subclasses.py GeneWikiWithRQFS.json output.json -iz -dp P31
```

### Add labels/descriptions for missing Q and P IDs to WDumper output
WDumper output will contain all information about items and properties that are explicitly specified in the input JSON file. Thus in any custom dump created by WDumper, there would be
a bunch of non-specified but used Q and P IDs as predicates and objects. Having at least labels and descriptions of these missed Q/P IDs can make WDumper outputs more useful.
Use `add_missing_QPid_labels.py` script as follows to **Add labels/descriptions for missing Q and P IDs to the WDumper output .nt files**:
Dependencies: `rdflib`
```
usage: add_missing_QPid_labels.py [-h] [-o OUTPUT] [-ip] input

positional arguments:
  input                 Input N-Triple file (WDumper decompressed output)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output destination file, enriched with the missing Q
                        IDs
  -ip, --includePids    Search for missing P IDs and add labels/descriptions
                        of them too
```
An example using the repo files will add labels and descriptions for missing Q IDs and P IDs (optional) to a decompressed WDumper .nt file:
```
python .\add_missing_QPid_labels.py .\therapeutic_use.nt -ip
