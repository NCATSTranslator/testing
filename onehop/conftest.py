import pytest
import os
import json

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
    metafunc.parametrize('TRAPI_case',edges, scope='session')

def pytest_generate_tests(metafunc):
    generate_TRAPI_KP_tests(metafunc)