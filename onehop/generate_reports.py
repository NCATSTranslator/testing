import csv
import bmt
import requests
import create_templates
import json
import yaml
from biothings_explorer.smartapi_kg.dataload import load_specs
import pprint
import pandas as pd

tk = bmt.Toolkit('https://raw.githubusercontent.com/biolink/biolink-model/1.7.0/biolink-model.yaml')
tsv_file = open("missing_predicates.tsv", "a")
tsv_missing_inverse = open("missing_inverses.csv", "a")
tsv_writer = csv.writer(tsv_file, delimiter='\t')
tsv_writer_inverse = csv.writer(tsv_missing_inverse)
inverses_header = ['subject', 'predicate', 'object', 'team', 'url']
tsv_writer_inverse.writerow([h for h in inverses_header])
missing_predicates = {}
m_pred_list = []


def aggregate_missing_predicates():
    specs = load_specs()
    for spec in specs:
        if 'x-translator' not in spec['info']:
            continue
        team = create_templates.get_team(spec)
        if 'servers' not in spec:
            pprint.pprint(spec.get('_meta'))
            pprint.pprint(spec.get('_status'))
            continue
        url = spec['servers'][0]['url']
        # this url just spins at the moment.
        # TODO: catch and report.
        if url == 'http://chp.thayer.dartmouth.edu/':
            continue
        if url.endswith('/'):
            url = url[:-1]
        predicates_url = f'{url}/predicates'
        is_trapi, predicates = create_templates.get_predicates(predicates_url)
        if is_trapi:
            dump_trapi_predicate_results(predicates_url, predicates, team)
        else:
            dump_smartapi_predicate_results(spec['info']['title'])
    with open(f'missing_predicates_with_teams.json', 'w') as predicates:
        data = []
        for predicate in missing_predicates:
            data.append({'predicate': predicate, 'teams': missing_predicates[predicate]})
        json.dump(data, predicates)
    with open(f'missing_details.json', 'w') as missing_details:
        json.dump(m_pred_list, missing_details)
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
        is_predicate, is_mixin, has_inverse = in_biolink_model(predicate)
        if x_translator is not None:
            for team in x_translator.get('team'):
                if is_predicate is False:
                    if predicate in missing_predicates:
                        if team not in missing_predicates[predicate]:
                            missing_predicates[predicate].append(team)
                        else:
                            missing_predicates[predicate] = [team]

                    tsv_writer.writerow([p_subject, predicate, p_object, team, url, is_mixin])
                    m_pred_list.append({"subject": p_subject,
                                        "predicate": predicate,
                                        "object": p_object,
                                        "team": team,
                                        "url": url,
                                        "is_mixin": is_mixin})
                else:
                    if has_inverse is False:
                        tsv_writer_inverse.writerow([p_subject, predicate, p_object, team, url])
                        m_pred_list.append({"subject": p_subject,
                                            "predicate": predicate,
                                            "object": p_object,
                                            "team": team,
                                            "url": url,
                                            "is_mixin": is_mixin})


def in_biolink_model(predicate):
    is_predicate = tk.is_predicate(predicate)
    is_mixin = tk.is_mixin(predicate)
    has_inverse = tk.has_inverse(predicate)
    return is_predicate, is_mixin, has_inverse


def dump_trapi_predicate_results(url, predicates, team):
        for source in predicates:
            for target in predicates[source]:
                for ptype in predicates[source][target]:
                    predicate = ptype
                    object = target
                    subject = source
                    is_predicate, is_mixin, has_inverse = in_biolink_model(predicate)
                    if is_predicate:
                        if has_inverse is False:
                            tsv_writer_inverse.writerow([subject, predicate, object, team, url])
                            m_pred_list.append({"subject": subject,
                                                "predicate": predicate,
                                                "object": object,
                                                "team": team,
                                                "url": url,
                                                "is_mixin": is_mixin})
                        continue
                    else:
                        if predicate in missing_predicates:
                            if url not in missing_predicates[predicate]:
                                missing_predicates[predicate].append(url)
                        else:
                            missing_predicates[predicate] = [url]
                        tsv_writer.writerow([subject, predicate, object, team, url, is_mixin])
                        m_pred_list.append({"subject": subject,
                                            "predicate": predicate,
                                            "object": object,
                                            "team": team,
                                            "url": url,
                                            "is_mixin": is_mixin})


if __name__ == '__main__':
    aggregate_missing_predicates()
