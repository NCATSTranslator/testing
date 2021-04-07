1. For Gene -> MolecularActivity: Use the following info to query using the NCBIGENE ID for DPH3 
```
fields: go.MF
species: human
requestBody:
  q: 285381    
  scopes: entrezgene
```
One of the answers should be metal ion binding, which has
```
go.MF.id: "GO:0046872"
```


2. For MolecularActivity -> Gene: Use the following info to query using the GO ID for structural constituent of bone 
```
fields: entrezgene
species: human
requestBody:
  q: "GO:0008147"    
  scopes: go.MF.id
  size: 1000
```
One of the answers should be MGP, which has
```
entrezgene: 4256
```


3. For Gene -> BiologicalProcess: Use the following info to query using the NCBIGENE ID for DPH3 
```
fields: go.BP
species: human
requestBody:
  q: 285381    
  scopes: entrezgene
```
One of the answers should be tRNA wobble uridine modification, which has
```
go.BP.id: "GO:0002098"
```


4. For BiologicalProcess -> Gene: Use the following info to query using the GO ID for regulation of carbohydrate utilization
```
fields: entrezgene
species: human
requestBody:
  q: "GO:0043610"    
  scopes: go.BP.id
  size: 1000
```
One of the answers should be MTOR, which has
```
entrezgene: 2475
```


5. For Gene -> CellularComponent: Use the following info to query using the NCBIGENE ID for DPH3 
```
fields: go.CC
species: human
requestBody:
  q: 285381    
  scopes: entrezgene
```
One of the answers should be nucleoplasm, which has
```
go.CC.id: "GO:0005654"
```


6. For CellularComponent -> Gene: Use the following info to query using the GO ID for node of Ranvier
```
fields: entrezgene
species: human
requestBody:
  q: "GO:0033268"    
  scopes: go.CC.id
  size: 1000
```
One of the answers should be SCN2A, which has
```
entrezgene: 6326
```


7. For Gene -> Pathway: Use the following info to query using the NCBIGENE ID for DPH3 
```
fields: pathway.reactome
species: human
requestBody:
  q: 285381    
  scopes: entrezgene
```
One of the answers should be Synthesis of diphthamide-EEF2, which has
```
pathway.reactome.id: "R-HSA-5358493"
```


8. For Pathway -> Gene: Use the following info to query using the REACT ID for Branched-chain amino acid catabolism
```
fields: entrezgene
species: human
requestBody:
  q: "R-HSA-70895"    
  scopes: pathway.reactome.id
  size: 1000
```
One of the answers should be SLC25A44, which has
```
entrezgene: 9673
```


9. For Gene -> Transcript: Use the following info to query using the ENSEMBL ID for KPNA5. Note BTE TRAPI endpoint for one API seems to have issues returning all of the expected results. 
```
fields: ensembl.transcript
species: human
requestBody:
  q: ENSG00000196911    
  scopes: ensembl.gene
```
One of the answers should be ENST00000413340, which has
```
ensembl.transcript: ENST00000413340
```


9. For Gene -> Protein: Use the following info to query using the ENSEMBL ID for KPNA5. Note BTE TRAPI endpoint for one API seems to have issues returning all of the expected results. 
```
fields: ensembl.protein
species: human
requestBody:
  q: ENSG00000196911    
  scopes: ensembl.gene
```
One of the answers should be ENSP00000396791, which has
```
ensembl.protein: ENSP00000396791
```


10. For Protein -> Gene: Use the following info to query using the UNIPROTKB ID for KPNA5
Note: The BTE TRAPI endpoint for one API is currently having issues successfully returning results. 
```
fields: ensembl.gene
species: human
requestBody:
  q: O15131   
  scopes: uniprot.Swiss-Prot
```
One of the answers should be KPNA5, which has
```
ensembl.gene: ENSG00000196911
```


11. For Gene -(homologous_to)-> Gene: Use the following info to query using the NCBIGENE ID for KCMF1. The x-bte extension currently isn't written to do the inverse operation (MGI in mice -> NCBIGENE in humans). 
```
fields: pantherdb.ortholog
requestBody:
  q: 56888    
  scopes: entrezgene
```
One of the answers should be mouse gene MGI 1921537, which has
```
pantherdb.ortholog.MGI: 1921537
```