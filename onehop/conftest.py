import pytest
import os
import json
from collections import defaultdict
from pytest_harvest import get_session_results_dct

def pytest_sessionfinish(session):
    """ Gather all results and save them to a csv.
    Works both on worker and master nodes, and also with xdist disabled"""

    session_results = get_session_results_dct(session)
    for t, v in session_results.items():
        if v['status'] == 'failed':
            outname = t.split('/')[-1][:-1]
            with open(f'{outname}.results','w') as outf:
                rb=v['fixtures']['results_bag']
                json.dump(rb['request'],outf,indent=4)
                outf.write(f'\nStatus Code: {rb["response"]["status_code"]}\n')
                json.dump(rb['response']['response_json'],outf,indent=4)

def pytest_addoption(parser):
    parser.addoption("--one", action="store_true", help="Only use first edge from each KP file")
    parser.addoption("--triple_source", action="store", help="Directory or file from which to retrieve triples")

def generate_TRAPI_KP_tests(metafunc):
    triple_source = metafunc.config.getoption('triple_source',default='test_triples/KP')
    edges = []
    idlist = []
    if not os.path.exists(triple_source):
        print("No such location:",triple_source)
        return edges
    if os.path.isfile(triple_source):
        filelist = [triple_source]
    else:
        filelist = []
        dtrips = os.walk(triple_source)
        for dirpath,dirnames,filenames in dtrips:
            for f in filenames:
                kpfile = f'{dirpath}/{f}'
                filelist.append(kpfile)
    for kpfile in filelist:
        with open(kpfile,'r') as inf:
            try:
                kpjson = json.load(inf)
            except:
                print('Invalid JSON')
                print(kpfile)
                exit()
        if kpjson['TRAPI']:
            for edge_i,edge in enumerate(kpjson['edges']):
                edge['api_name'] = kpfile.split('/')[-1]
                edge['url'] = kpjson['url']
                edges.append( edge )
                idlist.append( f'{kpfile}_{edge_i}')
                if metafunc.config.getoption('one'):
                    break
    if "KP_TRAPI_case" in metafunc.fixturenames:
        metafunc.parametrize('KP_TRAPI_case',edges,ids=idlist)
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
