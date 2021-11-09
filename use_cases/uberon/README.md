See https://github.com/obophenotype/uberon/wiki/Taxon-constraints for an explanation of modeling and reasoning over taxon constraints in Uberon.

The toy ontology in this folder uses:
* 6 classes anatomical structures
* 5 classes taxa
* 5 object properties

Both an OBO and an OWL version are provided here. Please note that the information provided in this ontology are not fully biologically correct, and does not faithfully represent the Uberon ontology. It only provides axioms to test the translation.

The important features are (description using OBO syntax):
* `UBERON:0003075 neural plate` only exists in `NCBITaxon:7711 Chordata`. Thanks to the disjoint classes axioms, we must infer that `UBERON:0003075 neural plate`, but also `UBERON:0000019 camera-type eye` (because there is a develops_from relation to neural plate), do not exist in `NCBITaxon:7586 Echinodermata` and `NCBITaxon:10219 Hemichordata`.
* `UBERON:0000050 simple eye with multiple lenses` never exists in `NCBITaxon:7711 Chordata`. We must then infer that `UBERON:0000050 simple eye with multiple lenses`, but also `UBERON:9999999 fake lens` (because there is a part_of relation to UBERON:0000050), do not exist in `NCBITaxon:7711 Chordata`, nor in `NCBITaxon:7742 Vertebrata` (because there is an is_a relation to NCBITaxon:7711).
* Note that the `DisjointClasses` axioms are necessary for the `only_in_taxon` relations to allow the expected reasoning.
* The "never_in_taxon" relations are expanded to EquivalentClass axioms to owl#Nothing, allowing the expected reasoning.
