import csv
import bmt
import requests
import create_templates
import json
from biothings_explorer.smartapi_kg.dataload import load_specs

tk = bmt.Toolkit('https://raw.githubusercontent.com/biolink/biolink-model/1.6.0/biolink-model.yaml')
tsv_file = open("missing_predicates.tsv", "a")
tsv_writer = csv.writer(tsv_file, delimiter='\t')
missing_predicates = {}


def aggregate_missing_predicates():
    specs = load_specs()
    for spec in specs:
        if not 'x-translator' in spec['info']:
            continue
        team = create_templates.get_team(spec)
        url = spec['servers'][0]['url']
        if url.endswith('/'):
            url = url[:-1]
        predicates_url = f'{url}/predicates'
        is_trapi, predicates = create_templates.get_predicates(predicates_url)
        if is_trapi:
            dump_trapi_predicate_results(predicates_url, predicates, team)
        else:
            dump_smartapi_predicate_results(spec['info']['title'])
    with open(f'missing_predicates_with_teams.json', 'w') as predicate_json:
        json.dump(missing_predicates, predicate_json, indent=4)
    with open('grouped_predicates.tsv', 'w') as fh:
        for key in missing_predicates:
            fh.write("%s,%s\n" % (key, missing_predicates[key]))


def dump_smartapi_predicate_results(apititle):
    """Create a template for a single REST-style KP smartAPI entry"""
    metakgurl = f'https://smart-api.info/api/metakg?api={apititle}'
    response = requests.get(metakgurl)
    for kgrecord in response.json()['associations']:
        p_subject = kgrecord.get('subject')
        p_object = kgrecord.get('object')
        predicate = kgrecord.get('predicate')
        api = kgrecord.get('api')
        smartapi = api.get('smartapi')
        url = smartapi.get('ui')
        x_translator = api.get('x-translator')

        if in_biolink_model(predicate):
            continue
        else:
            if x_translator is not None:
                for team in x_translator.get('team'):
                    if predicate in missing_predicates:
                        if team not in missing_predicates[predicate]:
                            missing_predicates[predicate].append(team)
                    else:
                        missing_predicates[predicate] = [team]
                    tsv_writer.writerow([p_subject, predicate, p_object, team, url])


def in_biolink_model(predicate):
    is_predicate = tk.is_predicate(predicate)
    return is_predicate


def dump_trapi_predicate_results(url, predicates, team):
        for source in predicates:
            for target in predicates[source]:
                for ptype in predicates[source][target]:
                    predicate = ptype
                    object = target
                    subject = source
                    if in_biolink_model(predicate):
                        continue
                    else:
                        if predicate in missing_predicates:
                            if url not in missing_predicates[predicate]:
                                missing_predicates[predicate].append(url)
                        else:
                            missing_predicates[predicate] = [url]
                        tsv_writer.writerow([subject, predicate, object, team, url])


if __name__ == '__main__':
    aggregate_missing_predicates()
