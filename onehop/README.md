# One-hop Tests

This suite tests our ability to retrieve given triples, which we know exist, from their KPs under a variety of transformations, both directly, and via ARAs.

The tests are generated from the files in `test_triples/KP`.  For each KP, it is quereied for the triples contained in its associated json file.  Then, ARAs are
queried for those triples according to the annotations in `test_triples/ARA` denoting from which KPs each ARA receives information.

## KP Instructions

For each KP, we need a file with one triple of each type that the KP can provide.  For instance, `test_triples/KP/Ranking_Agent/Automat_Human_GOA.json` contains the following json:
```{
    "url": "https://automat.renci.org/human-goa",
    "TRAPI": true,
    "edges": [
        {
            "subject_category": "biolink:Gene",
            "object_category": "biolink:BiologicalProcess",
            "predicate": "biolink:actively_involved_in",
            "subject": "NCBIGene:3949",
            "object": "GO:0006629"
        },
        {
            "subject_category": "biolink:Gene",
            "object_category": "biolink:MolecularActivity",
            "predicate": "biolink:enables",
            "subject": "NCBIGene:3949",
            "object": "GO:0005041"
        },
        {
            "subject_category": "biolink:Gene",
            "object_category": "biolink:CellularComponent",
            "predicate": "biolink:related_to",
            "subject": "NCBIGene:3949",
            "object": "GO:0034362"
        }
    ]
}
```

This KP provides three kinds of edges: Gene-actively_involved_in->BiologicalProcess, Gene-enables->MolecularActivity, and Gene-related_to->CellularComponent. For each of these kinds of edges, we have an entry in the file with a specific subject and object, and from these, we can create a variety of tests.

To aid KPs in creating these json files, we have generated templates in `templates/KP` using the predicates endpoint or smartAPI Registry MetaKG entries, which contains the edge types.  For instance, here is the template file associated with the human-goa KP:
```
{
    "url": "https://automat.renci.org/human-goa",
    "TRAPI": true,
    "edges": [
        {
            "subject_category": "biolink:Gene",
            "object_category": "biolink:BiologicalProcess",
            "predicate": "biolink:actively_involved_in",
            "subject": "",
            "object": ""
        },
        {
            "subject_category": "biolink:Gene",
            "object_category": "biolink:MolecularActivity",
            "predicate": "biolink:enables",
            "subject": "",
            "object": ""
        },
        {
            "subject_category": "biolink:Gene",
            "object_category": "biolink:CellularComponent",
            "predicate": "biolink:related_to",
            "subject": "",
            "object": ""
        }
    ]
}
```

Note that the templates are built from KP metadata and are a good starting place, but they are not necessarily a perfect match to the desired test triples.
In particular, if a template contains an entry for two edges, where one edge can be fully calculated given the other, then there is no reason to include 
test data for the derived edge.  For instance, there is no need to include test data for an edge in one direction, and its inverse in the other direction. Here
we will be assuming (and testing) the ability of the KP to handle inverted edges whether they are specified or not.  Similarly, if a KP has
"increases_expression_of" edges, there is no need to include "affects_expression_of" in the test triples, unless there is data that is only known at the
more general level.  If, say, there are triples where all that is known is an "affects_expression_of" predicate, then that should be included.

So the steps for a KP:
1. copy a template json from `templates` into a corresponding location in `test_triples`
2. filter out logically derivable template entries
3. fill in the subject and object entries for each triple with a real identifiers that should be retrievable from the KP

## ARA Instructions

For each ARA, we want to ensure that it is able to extract information correctly from the KPs.  To do this, we need to know which KPs each ARA interacts with.  We have generated template ARA json files under `templates/ARA` that contains annotations linking the ARA to all KPs.  For instance:

```
{
    "url": "https://strider.renci.org",
    "TRAPI": true,
    "KPs": [
        "Ontology-KP API",
        "CAM-KP API",
        "SRI Reference Knowledge Graph API",
        "Automat Cord19 Scigraph",
        "Automat Uberongraph",
        "Automat KEGG",
        "QuickGO API",
        "Automat Cord19 Scibite",
        "Automat HGNC",
        "OpenPredict API \ud83d\udd2e\ud83d\udc0d",
        "Automat GTEx",
        "Automat Human GOA",
        "Automat Viral Proteome",
        ... other kps here ...
        "Drug Response KP API",
        "BioLink API",
        "LINCS Data Portal API",
        "Columbia Open Health Data (COHD)",
        "Columbia Open Health Data (COHD) for COVID-19 Research",
        "Clinical Risk KP API"
    ]
}

```

In order to correctly link ARAs to KPs, ARAs will need to 
1. Copy the ARA template from `templates` to the corresponding place in `test_triples`
2. Edit the copied file to remove KPs that the ARA does not access.
3. If an ARA needs particular query options, these can also be added to the json (See Ranking_Agent/ARAGORN.json)

## Running Tests

Tests are implemented with pytest.  To run all tests, simply run
```
pytest test_onehops.py
```
But this takes quite some time, so frequently you will want to limit the tests run.

To run only KP tests:
```
pytest test_onehops.py::test_TRAPI_KPs
```

To run KP Tests, but only using one triple from each KP:
```
pytest test_onehops.py::test_TRAPI_KPs --one
```

To restrict test triples to those from a given directory or file:
```
pytest test_onehops.py::test_TRAPI_KPs --triple_source=<triple_source>
```
e.g.
```
pytest test_onehops.py::test_TRAPI_KPs --triple_source=test_triples/KP/Ranking_Agent
```
or
```
pytest test_onehops.py::test_TRAPI_KPs --triple_source=test_triples/KP/Ranking_Agent/Automat_CTD.json
```

To run only ARA tests (testing all ARAs for all KPs)
```
pytest test_onehops.py::test_TRAPI_ARAs
```

Options for restricting test triples for KPs also work for ARAs.  To test a single triple from the Automat CTD against all ARAs that use that KP:
```
pytest test_onehops.py::test_TRAPI_ARAs --one --triple_source=test_triples/KP/Ranking_Agent/Automat_CTD.json
```

The ARAs can also be restricted to a particular json or directory, e.g.
```
pytest test_onehops.py::test_TRAPI_ARAs --one --triple_source=test_triples/KP/Ranking_Agent/Automat_CTD.json --ARA_source=test_triples/ARA/Ranking_Agent/Strider.json
```