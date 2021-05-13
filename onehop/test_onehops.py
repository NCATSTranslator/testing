import pytest
import requests
from bmt import Toolkit
from reasoner_validator import validate_Message, ValidationError
import ontology_kp
from copy import deepcopy

#Toolkit takes a couple of seconds to initialize, so don't want it per-test
#note also that we are explictly controlling which version of biolink we are using.
tk = Toolkit('https://raw.githubusercontent.com/biolink/biolink-model/1.6.0/biolink-model.yaml')

def create_one_hop_message(edge, look_up_subject = False):
    """Given a complete edge, create a valid TRAPI message for querying for the edge.
    if look_up_subject is False (default) then the object id is not included, (lookup object
    by subject) and if look_up_subject is True, then the subject id is not included (look up
    subject by object)"""
    query_graph = {
        "nodes": {
            'a':{
                "category": edge['subject_category']
            },
            'b':{
                "category": edge['object_category']
            }
        },
        "edges": {
            'ab':{
                "subject": "a",
                "object": "b",
                "predicate": edge['predicate']
            }
        }
    }
    if look_up_subject:
        query_graph['nodes']['b']['id'] = edge['object']
    else:
        query_graph['nodes']['a']['id'] = edge['subject']
    message = {"message": {"query_graph": query_graph, 'knowledge_graph':{"nodes": {}, "edges": {},}, 'results':[]}}
    return message

####
##
## Functions for creating TRAPI messages from a known edge
##
## Each function returns the new message, and also some information used to evaluate whether the
## correct value was retrieved.  The second return value (object or subject) is the name of what is
## being returned and the third value (a or b) is which query node it should be bound to in one of the
## results.  For example, when we look up a triple by subject, we should expect that the object entity
## is bound to query node b.
##

def by_subject(request):
    """Given a known triple, create a TRAPI message that looks up the object by the subject"""
    message = create_one_hop_message(request, look_up_subject=False)
    return message, 'object', 'b'

def by_object(request):
    """Given a known triple, create a TRAPI message that looks up the subject by the object"""
    message = create_one_hop_message(request, look_up_subject=True)
    return message, 'subject', 'a'

def inverse_by_new_subject(request):
    """Given a known triple, create a TRAPI message that inverts the predicate, then looks up the new
    object by the new subject (original object)"""
    original_predicate_element = tk.get_element(request['predicate'])
    if original_predicate_element['symmetric']:
        transformed_predicate = request['predicate']
    else:
        transformed_predicate_name = original_predicate_element['inverse']
        if transformed_predicate_name is None:
            transformed_predicate = None
        else:
            tp = tk.get_element(transformed_predicate_name)
            transformed_predicate = tp.slot_uri
    #Not everything has an inverse (it should, and it will, but it doesn't right now)
    if transformed_predicate is None:
        return None, None, None
    transformed_request = {
        "url": "https://automat.renci.org/human-goa",
        "subject_category": request['object_category'],
        "object_category": request['subject_category'],
        "predicate": transformed_predicate,
        "subject": request['object'],
        "object": request['subject']
    }
    message = create_one_hop_message(transformed_request, look_up_subject=False)
    #We inverted the predicate, and will be querying by the new subject, so the output will be in node b
    # but, the entity we are looking for (now the object) was originally the subject because of the inversion.
    return message, 'subject', 'b'

def raise_predicate_by_subject(request):
    """Given a known triple, create a TRAPI message that uses the parent of the original predicate and looks up
    the object by the subject"""
    transformed_request = request.copy() #there's no depth to request, so it's ok
    if request['predicate'] != 'biolink:related_to':
        original_predicate_element = tk.get_element(request['predicate'])
        parent = tk.get_element(original_predicate_element['is_a'])
        transformed_request['predicate'] = parent['slot_uri']
    message = create_one_hop_message(transformed_request, look_up_subject=False)
    return message, 'object', 'b'

def raise_object_by_subject(request):
    """Given a known triple, create a TRAPI message that uses the parent of the original object category and looks up
    the object by the subject"""
    original_object_element = tk.get_element(request['object_category'])
    transformed_request = request.copy() #there's no depth to request, so it's ok
    parent = tk.get_element(original_object_element['is_a'])
    transformed_request['object_category'] = parent['class_uri']
    message = create_one_hop_message(transformed_request, look_up_subject=False)
    return message, 'object', 'b'

def raise_subject_entity(request):
    """Given a know triple create a TRAPI message that uses the parent of the original entity and looks up the object"""
    subject_cat = request['subject_category']
    subject = request['subject']
    parent_subject = ontology_kp.get_parent(subject, subject_cat)
    if parent_subject is None:
        print('No Parent: ',subject)
        return None
    mod_request = deepcopy(request)
    mod_request['subject'] = parent_subject
    message = create_one_hop_message(mod_request, look_up_subject=False)
    return message, 'object', 'b'

##
## End TRAPI creating functions
##
############
############

def callTRAPI(url,opts,trapi_message):
    """Given an url and a TRAPI message, post the message to the url and return the status and json response"""
    query_url = f'{url}/query'
    print(query_url)
    response = requests.post(query_url,json=trapi_message,params=opts)
    try:
        response_json = response.json()
    except:
        response_json = None
    return {'status_code':response.status_code, 'response_json': response_json}

def is_valid_TRAPI(response_json):
    """Make sure that the Message is valid using reasoner_validator"""
    try:
        validate_Message(response_json)
        return True
    except ValidationError as e:
        import json
        #print(json.dumps(response_json,indent=4))
        print(e)
        return False

def check_provenance(ARA_case, ARA_response):
    """This is where we will check to see whether the edge in the ARA response is marked with the expected
    KP.  But at the moment, there is not a standard way to do this."""
    pass

def execute_TRAPI_lookup(case,creator,rbag):
    #Create TRAPI query/response
    rbag.location = case['location']
    rbag.case = case
    TRAPI_request, output_element, output_node_binding = creator(case)
    if TRAPI_request is None:
        #The particular creator cannot make a valid message from this triple
        return None
    if not is_valid_TRAPI(TRAPI_request['message']):
        #This is a problem with the testing framework.
        exit()
    TRAPI_response  = callTRAPI(case['url'],case['query_opts'],TRAPI_request)
    #Successfully invoked the query endpoint
    rbag.request  = TRAPI_request
    rbag.response = TRAPI_response
    assert TRAPI_response['status_code'] == 200
    #Got back valid TRAPI Response
    response_message = TRAPI_response['response_json']['message']
    assert is_valid_TRAPI(response_message)
    #The response had results
    assert len( response_message['results'] ) > 0
    #The results contained the object of the query
    object_ids = [r['node_bindings'][output_node_binding][0]['id'] for r in response_message['results']]
    assert case[output_element] in object_ids
    return response_message


#@pytest.mark.parametrize("trapi_creator", [by_subject, by_object, raise_subject_entity, raise_object_by_subject, raise_predicate_by_subject])
def test_TRAPI_KPs(KP_TRAPI_case,trapi_creator,results_bag):
    """Generic Test for TRAPI KPs. The KP_TRAPI_case fixture is created in conftest.py by looking at the test_triples
    These get successively fed to test_TRAPI.  This function is further parameterized by trapi_creator, which knows
    how to take an input edge and create some kind of TRAPI query from it.  For instance, by_subject removes the object,
    while raise_object_by_subject removes the object and replaces the object category with its biolink parent.
    This approach will need modification if there turn out to be particular elements we want to test for different
    creators.
    """
    execute_TRAPI_lookup(KP_TRAPI_case,trapi_creator,results_bag)

@pytest.mark.parametrize("trapi_creator", [by_subject, by_object, raise_subject_entity, raise_object_by_subject, raise_predicate_by_subject])
def test_TRAPI_ARAs(ARA_TRAPI_case, trapi_creator, results_bag):
    """Generic Test for ARA TRAPI.  It does the same thing as the KP trapi, calling an ARA that should be pulling
    data from the KP.
    Then it performs a check on the result to make sure that the source is correct.
    Currently, that provenance check is a short circuit since ARAs are not reporting this in a standard way yet.
    """
    response_message = execute_TRAPI_lookup(ARA_TRAPI_case,trapi_creator, results_bag)
    if response_message is not None:
        check_provenance(ARA_TRAPI_case,response_message)