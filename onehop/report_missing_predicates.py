import csv
import bmt
import requests
import create_templates
from biothings_explorer.smartapi_kg.dataload import load_specs

tk = bmt.Toolkit('https://raw.githubusercontent.com/biolink/biolink-model/1.6.0/biolink-model.yaml')
tsv_file_trapi = open("missing_predicates_trapi.tsv", "w")
tsv_file_metakg = open("missing_predicates_metakg.tsv", "w")
tsv_writer_metakg = csv.writer(tsv_file_metakg, delimiter='\t')
tsv_writer_trapi = csv.writer(tsv_file_trapi, delimiter='\t')

def aggregate_missing_predicates():
    specs = load_specs()
    for spec in specs:
        if not 'x-translator' in spec['info']:
            continue
        url = spec['servers'][0]['url']
        apititle = '_'.join(spec['info']['title'].split())
        if url.endswith('/'):
            url = url[:-1]
        predicates_url = f'{url}/predicates'
        is_trapi, predicates = create_templates.get_predicates(predicates_url)
        if is_trapi:
            dump_trapi_predicate_results(predicates_url, predicates)
        else:
            dump_smartapi_predicate_results(spec['info']['title'])


def dump_smartapi_predicate_results(apititle):
    """Create a template for a single REST-style KP smartAPI entry"""
    metakgurl = f'https://smart-api.info/api/metakg?api={apititle}'
    response = requests.get(metakgurl)
    for kgrecord in response.json()['associations']:
        subject = kgrecord.get('subject')
        object = kgrecord.get('object')
        predicate = kgrecord.get('predicate')
        api = kgrecord.get('api')
        x_translator = api.get('x-translator')
        if in_biolink_model(predicate):
            continue
        else:
            if x_translator is not None:
                for team in x_translator.get('team'):
                    tsv_writer_metakg.writerow([subject, predicate, object, team])


def in_biolink_model(predicate):
    is_predicate = tk.is_predicate(predicate)
    return is_predicate


def dump_trapi_predicate_results(url, predicates):
        for source in predicates:
            for target in predicates[source]:
                for ptype in predicates[source][target]:
                    predicate = ptype
                    object = target
                    subject = source
                    if in_biolink_model(predicate):
                        continue
                    else:
                        tsv_writer_trapi.writerow([subject, predicate, object, url])


if __name__ == '__main__':
    aggregate_missing_predicates()
