These KPs are not TRAPI APIs. 

The tests described in the JSON files are written as-if these are TRAPI APIs. The expectation there is that a TRAPI query is made through BTE (the endpoint /v1/smartapi/{smartapi_id}/query) using the info in the JSON files. The edge to the "answer" node should have an attribute with the name "api" and value as the name of the API. 

Notes:
- tests are also described as queries that can be made directly to the API, in the additional README files. Notice that many API endpoints do not handle curies (ID prefixes) or predicates. The format of these queries is specified by the x-bte-annotated endpoint in the SmartAPI registry file. 
- predicates may change over time, as we change our biolink predicate choices and as the biolink model predicates change