1. For Disease -> Gene: Use the following info to query using the UMLS ID for Leigh Disease. 
```
fields: disgenet.genes_related_to_disease
requestBody:
  q: C0023264    
  scopes: mondo.xrefs.umls, disgenet.xrefs.umls
```
One of the answers should be NDUFA1, which has
```
disgenet.genes_related_to_disease.gene_id: 4694
```


2. For Disease -> Variant: Use the following info to query using the UMLS ID for Leigh Disease. 
Note: This operation's output ID is different than in the BTE interface (HGVS:NC_000016.10:g.1772798C>A). 
```
fields: disgenet.variants_related_to_disease
requestBody:
  q: C0023264    
  scopes: mondo.xrefs.umls, disgenet.xrefs.umls
```
One of the answers should be rs1161932777, which has
```
disgenet.variants_related_to_disease.rsid: rs1161932777
```


3. For Disease -> PhenotypicFeature: Use the following info to query using the OMIM ID for Dihydrolipoamide Dehydrogenase Deficiency
Note: This operation's output ID is different than in the BTE interface (UMLS:C0023380). 
```
fields: hpo.phenotype_related_to_disease   
requestBody:
  q: 246900    
  scopes: hpo.omim
```
One of the answers should be Lethargy, which has
```
hpo.phenotype_related_to_disease.hpo_id: HP:0001254
```


4. For Disease -> ChemicalSubstance: Use the following info to query using the MESH ID for Multiple Organ Failure
Note: This operation's output ID is different than in the BTE interface (CHEBI:65324).
```
fields: ctd.chemical_related_to_disease
requestBody:
  q: D009102    
  scopes: ctd.mesh
```
One of the answers should be 17-(dimethylaminoethylamino)-17-demethoxygeldanamycin, which has
```
ctd.chemical_related_to_disease.mesh_chemical_id: C448659
```


5. For Gene -> Disease: Use the following info to query using the NCBIGENE ID for DBT
```
fields: disgenet.xrefs.umls
size: 1000
requestBody:
  q: 1629    
  scopes: disgenet.genes_related_to_disease.gene_id
```
One of the answers should be Drug-Induced Acute Liver Injury, which has
```
disgenet.xrefs.umls: C3658290
```


6. For Variant -> Disease: Use the following info to query using the DBSNP ID rs78655421
```
fields: disgenet.xrefs.umls
size: 1000
requestBody:
  q: rs78655421    
  scopes: disgenet.variants_related_to_disease.rsid
```
One of the answers should be Non-obstructive azoospermia, which has
```
disgenet.xrefs.umls: C4021107
```


7. For PhenotypicFeature -> Disease: Use the following info to query using the HP ID for Hypogeusia
Note: This operation's output ID is different than in the BTE interface (MONDO:0012107).
```
fields: hpo.omim
size: 1000
requestBody:
  q: "HP:0000224"    
  scopes: hpo.phenotype_related_to_disease.hpo_id
```
One of the answers should be Neuropathy, Hereditary Sensory And Autonomic, Adult-onset, With Anosmia, which has
```
hpo.omim: 608720
```


8. For ChemicalSubstance -> Disease: Use the following info to query using the MESH ID for Amodiaquine
```
fields: ctd.mesh
size: 1000
requestBody:
  q: D000655
  scopes: ctd.chemical_related_to_disease.mesh_chemical_id
```
One of the answers should be Anorexia, which has
```
ctd.mesh: D000855
```


9. For Disease -(superclass_of)-> Disease: Use the following info to query using the MONDO ID for substance-related disorder
```
fields: mondo.descendants
size: 1000
requestBody:
  q: "MONDO:0002494"
  scopes: mondo.mondo
```
One of the answers should be alcoholic pancreatitis, which has
```
mondo.descendants: "MONDO:0003232"
```


10. For Disease -(subclass_of)-> Disease: Use the following info to query using the MONDO ID for substance-related disorder
```
fields: mondo.parents
size: 1000
requestBody:
  q: "MONDO:0002494"
  scopes: mondo.mondo
```
One of the answers should be psychiatric disorder, which has
```
mondo.descendants: "MONDO:0002025"
```