## Wikidata Lipids Subset

The aim of this use case is to make a subset of Wikidata that contains all the chemical compounds having a LipidMaps ID.

Below is the ShEx template to validate the extracted entities and only the passing ones will end up in the subset.

![ShEx template visualization](lipids.shex.png?raw=true)

## Predicates used
* https://www.wikidata.org/wiki/Property:P2063
* https://www.wikidata.org/wiki/Property:P234
* https://www.wikidata.org/wiki/Property:P235
* https://www.wikidata.org/wiki/Property:P703


## Obtaining the subset

Please run the wikidata-lipids-slurper.ipynb notebook and the output will be a collection of ttl files.

The files the can be loaded into your triple store of choice. 
