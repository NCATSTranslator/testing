1. For ChemicalSubstance -(metabolic_processing_affected_by)-> Gene: Use the following info to query using the DRUGBANK ID for Cannabidiol. 
Note: This operation's output ID is different than in the BTE interface (NCBIGENE:1543). 
```
fields: drugbank.enzymes
requestBody:
  q: DB09061    
  scopes: drugbank.id
```
One of the answers should be CYP1A1, which has
```
drugbank.enzymes.gene_name: CYP1A1
```


2. For Gene -(affects_metabolic_processing_of)-> ChemicalSubstance: Use the following info to query using the SYMBOL for CYP1A1. 
Note: This operation's output ID is different than in the BTE interface (CHEBI:34545). 
```
fields: drugbank.id
size: 1000
requestBody:
  q: CYP1A1    
  scopes: drugbank.enzymes.gene_name
```
One of the answers should be Azimilide, which has 
```
drugbank.enzymes.gene_name: DB04957
```


3. For ChemicalSubstance -(physically_interacts_with)-> Gene: Use the following info to query using the DRUGBANK ID for Halothane. 
Note: This operation's output ID is different than in the BTE interface (NCBIGENE:3783). 
```
fields: drugbank.targets
requestBody:
  q: DB01159    
  scopes: drugbank.id
```
One of the answers should be KCNN4, which has
```
drugbank.targets.gene_name: KCNN4
```


4. For Gene -(physically_interacts_with)-> ChemicalSubstance: Use the following info to query using the SYMBOL for KCNN4. 
Note: This operation's output ID is different than in the BTE interface (CHEBI:7582). 
```
fields: chembl.molecule_chembl_id
size: 1000
requestBody:
  q: KCNN4    
  scopes: drugcentral.bioactivity.uniprot.gene_symbol
```
One of the answers should be NITRENDIPINE, which has 
```
chembl.molecule_chembl_id: CHEMBL475534
```


5. For ChemicalSubstance -(approved_to_treat)-> Disease: Use the following info to query using the CHEMBL.COMPOUND ID for METHYLPREDNISOLONE. 
Note: This operation's output ID is different than in the BTE interface (MONDO:0015129). 
```
fields: drugcentral.drug_use.indication
requestBody:
  q: CHEMBL650    
  scopes: chembl.molecule_chembl_id
```
One of the answers should be Primary adrenocortical insufficiency, which has
```
drugcentral.drug_use.indication.umls_cui: C0001403
```


6. For Disease -(approved_for_treatment_by)-> ChemicalSubstance: Use the following info to query using the UMLS ID for Ankylosing spondylitis. 
Note: This operation's output ID is different than in the BTE interface (CHEBI:6888). 
```
fields: chembl.molecule_chembl_id
size: 1000
requestBody:
  q: C0038013    
  scopes: drugcentral.drug_use.indication.umls_cui
```
One of the answers should be METHYLPREDNISOLONE, which has
```
chembl.molecule_chembl_id: CHEMBL650
```


7. For ChemicalSubstance -(contraindicated_for)-> Disease: Use the following info to query using the CHEMBL.COMPOUND ID for OSELTAMIVIR. 
```
fields: drugcentral.drug_use.contraindication
requestBody:
  q: CHEMBL1229    
  scopes: chembl.molecule_chembl_id
```
One of the answers should be Impaired cognition, which has
```
drugcentral.drug_use.contraindication.umls_cui: C0338656
```


8. For Disease -(is_contraindication_for)-> ChemicalSubstance: Use the following info to query using the UMLS ID for Primary adrenocortical insufficiency. 
Note: This operation's output ID is different than in the BTE interface (CHEBI:91591). 
```
fields: chembl.molecule_chembl_id
size: 1000
requestBody:
  q: C0001403
  scopes: drugcentral.drug_use.contraindication.umls_cui
```
One of the answers should be pheniramine, which has
```
chembl.molecule_chembl_id: CHEMBL1193
```