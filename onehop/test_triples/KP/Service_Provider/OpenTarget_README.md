1. For Gene -> ChemicalSubstance: Use the following info to query using the ENSEMBL ID for FKBP1A 
Note: This operation's output ID (the full identifier CHEMBL) is different than in the BTE interface (CHEBI:68478). 
```
parameters:
  target: ENSG00000088832
  datasource: chembl
  size: 100
  fields: drug
```
One of the answers should be EVEROLIMUS, which has
```
data.drug.id: "http://identifiers.org/chembl.compound/CHEMBL1908360"
```

Note: BTE TRAPI is currently having an issue. The raw output of this API is very redundant, and it seems that this is causing issues with the results section of the response (nodes and edges are fine). 