import pytest
import os
import json
from collections import defaultdict

def generate_TRAPI_KP_tests(metafunc):
    dtrips = os.walk('test_triples/KP')
    edges = [ ]
    for dirpath,dirnames,filenames in dtrips:
        for f in filenames:
            kpfile = f'{dirpath}/{f}'
            with open(kpfile,'r') as inf:
                kpjson = json.load(inf)
            if kpjson['TRAPI']:
                for edge in kpjson['edges']:
                    edge['api_name'] = f
                    edge['url'] = kpjson['url']
                    edges.append( edge )
    if "KP_TRAPI_case" in metafunc.fixturenames:
        metafunc.parametrize('KP_TRAPI_case',edges)
    return edges

#Once the smartapi tests are up, we'll want to pass them in here as well
def generate_TRAPI_ARA_tests(metafunc,kp_edges):
    if "ARA_TRAPI_case" not in metafunc.fixturenames:
        return
    kp_dict = defaultdict(list)
    for e in kp_edges:
        #eh, not handling api name very well
        kp_dict[e['api_name'][:-5]].append(e)
    dtrips = os.walk('test_triples/ARA')
    ara_edges = []
    #Figure out which ARAs should be able to get which triples from which KPs
    for dirpath,dirnames,filenames in dtrips:
        for f in filenames:
            arafile = f'{dirpath}/{f}'
            with open(arafile,'r') as inf:
                arajson = json.load(inf)
            for kp in arajson['KPs']:
                for kp_edge in kp_dict['_'.join(kp.split())]:
                    edge = kp_edge.copy()
                    edge['api_name'] = f
                    edge['url'] = arajson['url']
                    edge['kp_source'] = kp
                    ara_edges.append( edge )
    metafunc.parametrize('ARA_TRAPI_case', ara_edges)

def pytest_generate_tests(metafunc):
    """This hook is run at test generation time.  These functions look at the configured triples on disk
    and use them to parameterize inputs to the test functions. Note that this gets called multiple times, once
    for each test_* function, and you can only parameterize an argument to that specific test_* function.
    However, for the ARA tests, we still need to get the KP data, since that is where the triples live."""
    TRAPI_KP_edges = generate_TRAPI_KP_tests(metafunc)
    generate_TRAPI_ARA_tests(metafunc,TRAPI_KP_edges)