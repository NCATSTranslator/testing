These are not TRAPI APIs. As a result, this is what we suggest:

- subject and object are given with the ID format the API expects. They may NOT be curies. The x-bte info in the SmartAPI registry files describes the ID namespaces with Translator-compliant prefixes
- query them according to the x-bte information in the SmartAPI Registry. The x-bte info includes what endpoint to use and what to put for the various parameters/request-body
- the input will be the subject's ID (no predicate or object)
- the predicate may change over time, as we change our biolink predicate choices and as the biolink model predicates change

MyDisease.info:  
- Disease -> PhenotypicFeature: subject is OMIM (use hpo.omim in scopes)
- Disease -> ChemicalSubstance: subject is MESH (use ctd.mesh in scopes)
- PhenotypicFeature -> Disease: object is OMIM (use hpo.omim in fields)
- ChemicalSubstance -> Disease: object is MESH (use ctd.mesh in fields)
