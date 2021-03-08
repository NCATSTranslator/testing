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

So the steps for a KP:
1. copy a template json from `templates` into a corresponding location in `test_triples`
2. fill in the subject and object entries for each triple with a real identifiers that should be retrievable from the KP

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
