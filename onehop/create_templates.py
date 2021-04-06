from biothings_explorer.smartapi_kg.dataload import load_specs
from biothings_explorer.smartapi_kg import MetaKG
import os
import requests
import json


def get_team(spec):
    """Retrieve the team from a smartAPI entry"""
    teams = spec['info']['x-translator']['team']
    # Some of these are strings, some are lists...
    if isinstance(teams, str):
        teams = [teams]
    if len(teams) > 1:
        # Some KPs are collaborative.  For the current situation, we want to assign a single owner.
        # I think all the current shared KPs are collabs with Service Provider
        teams.remove('Service Provider')
    if len(teams) > 1:
        raise Exception('What do you want to do about multi-team KPs?')
    team = teams[0]
    return team

def get_predicates(pr_url):
    """Collect the /predicates endpoint for a TRAPI-style KP smartAPI entry"""
    try:
        #print(pr_url)
        response = requests.get(pr_url)
        if response.status_code == 200:
            return True,response.json()
        else:
            return False,{}
    except:
        return False,{}

def create_ARA_template(spec,kp_titles):
    """Create a template for an ARA denoting the KPs it calls"""
    team = get_team(spec)
    teamdir = (f'templates/ARA/{"_".join(team.split())}')
    if not os.path.exists(teamdir):
        os.makedirs(teamdir)
    apititle = '_'.join(spec['info']['title'].split())
    try:
        output = { "url": spec['servers'][0]['url'],
                   "TRAPI": True,
                   "KPs": kp_titles}
        with open(f'{teamdir}/{apititle}.json', 'w') as outf:
            json.dump(output, outf, indent=4)
    except:
        print (f'Failed {apititle}: invalid spec')


def create_trapi_template(teamdir, apititle, url, predicates):
    """Create a template for a single TRAPI-style KP smartAPI entry"""
    edges = []
    for source in predicates:
        for target in predicates[source]:
            for ptype in predicates[source][target]:
                edges.append( {'subject_category':source,
                               'object_category':target,
                               'predicate': ptype,
                               'subject': '',
                               'object': ''})
    sources = predicates
    output = { "url": url,
               "TRAPI": True,
               "edges": edges}
    with open(f'{teamdir}/{apititle}.json','w') as outf:
        json.dump(output,outf,indent=4)

def create_smartapi_template(teamdir, apititle, url):
    """Create a template for a single REST-style KP smartAPI entry"""
    metakgurl = f'https://smart-api.info/api/metakg?api={apititle}'
    response = requests.get(metakgurl)
    predicates = response.json()['associations']
    edges = []
    for p in predicates:
        edges.append({'subject_category': f'biolink:{p["subject"]}',
                      'object_category': f'biolink:{p["object"]}',
                      'predicate': f'biolink:{p["predicate"]}',
                      'subject': '',
                      'object': ''})
    if len(edges) == 0:
        print('This API does not have a predicate, and has no edges in MetaKG:', apititle, url)
    output = { "url": url,
               "TRAPI": False,
               "edges": edges}
    with open(f'{teamdir}/{"_".join(apititle.split())}.json','w') as outf:
        json.dump(output,outf,indent=4)

def create_KP_template(spec):
    """Create a template for a single KP smartAPI entry"""
    team = get_team(spec)
    teamdir = (f'templates/KP/{"_".join(team.split())}')
    if not os.path.exists(teamdir):
        os.makedirs(teamdir)
    apititle = '_'.join(spec['info']['title'].split())
    url = spec['servers'][0]['url']
    #At the moment, there's no way to tell whether this is a TRAPI or not
    #some url cleanup
    if url.endswith('/'):
        url = url[:-1]
    predicates_url =  f'{url}/predicates'
    is_trapi, predicates = get_predicates(predicates_url)
    if is_trapi:
        create_trapi_template(teamdir,apititle,url,predicates)
    else:
        create_smartapi_template(teamdir,spec['info']['title'],url)

def create_template(spec):
    """Create a template for a single smartAPI entry"""
    if spec['info']['x-translator']['component'] == 'Utility':
        return
    if spec['info']['x-translator']['component'] == 'ARA':
        create_ARA_template(spec)
    if spec['info']['x-translator']['component'] == 'KP':
        create_KP_template(spec)

def create_templates():
    """Create Templates for each KP and ARA to fill in"""
    specs = load_specs()
    #print(len(specs))
    kp_titles = []
    #loop twice.  Once to get the KPs and collect their names and then once to get the ARAs
    for spec in specs:
        if not 'x-translator' in spec['info']:
            continue
        if spec['info']['x-translator']['component'] == 'KP':
            create_KP_template(spec)
            kp_titles.append(spec['info']['title'])
    for spec in specs:
        if not 'x-translator' in spec['info']:
            continue
        if spec['info']['x-translator']['component'] == 'ARA':
            create_ARA_template(spec,kp_titles)

#There should be a path that checks to see if there's already a test_triples for the source and only checks to see
# if it needs to be modified?  Or in general need some better idea of change management.
if __name__ == '__main__':
    create_templates()
