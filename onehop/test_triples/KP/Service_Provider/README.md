The JSON files assume that these APIs will be queried through BTE's TRAPI endpoint for querying individual SmartAPIs (accessible through the URLs provided). 

Notes:
- tests are also described as queries that can be made directly to the API, in the additional README files. Notice that many API endpoints do not handle curies (ID prefixes) or predicates. The format of these queries is specified by the x-bte-annotated endpoint in the SmartAPI registry file. 
- predicates may change over time, as we change our biolink predicate choices and as the biolink model predicates change