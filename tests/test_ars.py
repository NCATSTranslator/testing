"""Test ARS et all."""
import json
import os
import httpx
import pytest
import asyncio
import requests
import logging
# We really shouldn't be doing this, but just for now...
from requests.packages.urllib3.exceptions import InsecureRequestWarning

logging.basicConfig(filename='test_ars.log', level=logging.DEBUG)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ARS_URL="https://ars.transltr.io/ars/api/"
ARS_URL = "https://ars-dev.transltr.io/ars/api/"
# BASE_PATH=os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))
)
NORMALIZER_URL = "https://nodenormalization-sri.renci.org/get_normalized_nodes"


def keys_exist(element, *keys):
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
            if _element is None:
                return False
        except KeyError:
            return False
    return True


def get_safe(element, *keys):
    """
    :param element: JSON to be processed
    :param keys: list of keys in order to be traversed. e.g. "fields","data","message","results
    :return: the value of the terminal key if present or None if not
    """
    if element is None:
        return None
    _element = element
    for key in keys:
        try:
            _element = _element[key]
            if _element is None:
                return None
            if key == keys[-1]:
                return _element
        except KeyError:
            return None
    return None


def get_files(relativePath):
    logging.debug("get_files")
    files = []
    my_dir = BASE_PATH+relativePath
    for filename in os.listdir(my_dir):
        files.append(os.path.join(my_dir,filename))
    return files


@pytest.mark.asyncio
async def test_not_none(caplog):
    caplog.set_level(logging.ERROR)
    logging.debug("test_not_none")
    print ("+++ +++ CHECKING FOR NON-ZERO RESULTS")
    files = get_files("/ars-requests/not-none")
    report_cards = []
    for file in files:
        print("+++ Checking "+file+" for non-zero result counts")
        logging.debug("+++ File is as follows: \n")
        with open(file, "r") as f:
            query = json.load(f)
            logging.debug(json.dumps(query, indent=4, sort_keys=True))
            report_card = await has_results(query)
            print(json.dumps(report_card,indent=4,sort_keys=True))
            report_cards.append(report_card)
    for card in report_cards:
        for agent, grade in card.items():
            assert grade=="Pass"
    return report_cards


@pytest.mark.asyncio
async def test_must_have_curie(caplog):
    caplog.set_level(logging.ERROR)
    print(" +++ +++ CHECKING FOR SPECIFIC RESULTS")
    logging.debug("test_must_have_curie")
    answers_filename = "answers.json"
    dir = BASE_PATH+"/ars-requests/must-have"
    report_cards =[]

    answers_file= os.path.join(dir,answers_filename)
    with open(answers_file,"r") as f:
        answers_list=json.load(f)
    for query_file,answers in answers_list.items():
        with open(dir+"/"+query_file) as f:
            query = json.load(f)
        print("+++ Checking "+query_file+ " for "+str(answers))
        report_card = await must_contain_curie(answers,query)
        print(json.dumps(report_card, indent=4, sort_keys=True))
        report_cards.append(report_card)
    for card in report_cards:
        for agent, grade in card.items():
            assert grade=="Pass"


async def call_ars(payload, url=ARS_URL+"submit"):
    logging.debug("call_ars")
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            url,
            json=payload,
            timeout=60.0,
        )
    response.raise_for_status()
    return response.json()


async def must_contain_curie(curies,query):
    logging.debug("must_contain_curie")
    logging.debug("curies ="+str(curies))
    logging.debug("query= "+json.dumps(query, indent=4, sort_keys=True))
    children = await get_children(query)
    synonyms = []
    for curie in curies:
        syns = get_synonyms(curie)
        synonyms.extend(syns)
    report_card = {}
    for entry in children:
        passed = False
        agent = entry[0]
        child = entry[1]
        logging.debug("agent "+agent)
        nodes = get_safe(child,"fields","data","message","knowledge_graph","nodes")
        if nodes is not None:
            # logging.debug("nodes: "+str(nodes))
            logging.debug("looking for "+str(synonyms))
            logging.debug("nodes "+str(nodes.keys()))
            passed = any(item in synonyms for item in nodes.keys())
        if passed:
            report_card[agent]="Pass"
        else:
            report_card[agent]="Fail"
    return report_card


async def has_results(query):
    logging.debug("has_results")
    report_card = {}
    children = await get_children(query)
    for child in children:
        passed = False
        agent = child[0]
        childData=child[1]
        results = get_safe(childData,"fields","data","message","results")
        if(results is not None):
            if(len(results)>0):
                logging.debug(agent+ " has "+str(len(results))+" results")
                passed = True
            else:
                logging.debug(agent +" has no results for this query")
        else:
            status = get_safe(childData,"fields","status")
            # print(agent +" has no results for this query.  Status reported as: "+status+"\n"
            #             "Further details in log file.")
            logging.warning("++++ "+agent+" had a status of "+status+" for query")
            logging.warning(json.dumps(query, indent=4, sort_keys=True))
            logging.warning("Full response is as follows:")
            logging.warning(json.dumps(childData, indent=4, sort_keys=True))
        if passed:
            report_card[agent]="Pass"
        else:
            report_card[agent]="Fail"
    return report_card


async def get_children(query, url=None, timeout=None):
    logging.debug("get_children")
    children = []
    response = await call_ars(query)
    pk = response['pk']
    if url is None:
        url = ARS_URL+"messages/"+pk+"?trace=y"
    if timeout is None:
        timeout = 60
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.get(
            url,
            timeout=10.0
        )
    data = r.json()
    for child in data['children']:
        agent = child['actor']['agent']
        childPk=child['message']
        logging.debug("---Checking child for "+agent+", pk="+pk)
        childData = await get_child(childPk)
        children.append(
            [agent,childData]
        )
    return children


async def get_child(pk,timeout=60):
    logging.debug("get_child("+pk+")")
    wait_time = 5  # amount of seconds to wait between checks for a Running query result
    url = ARS_URL+"messages/"+pk
    async with httpx.AsyncClient(verify=False) as client:
        child= await client.get(
            url,
            timeout=10.0
        )
        data=child.json()
        status = get_safe(data, "fields", "status")
        if status is not None:
            if status == "Done":
                return data
            elif status == "Running":
                if timeout>0:
                    logging.debug("Query response is still running\n"
                                  + "Wait time remaining is now "+str(timeout)+"\n"
                                  + "What we have so far is: "
                                  + json.dumps(data, indent=4, sort_keys=True))
                    await asyncio.sleep(wait_time)
                    return await get_child(pk, timeout-wait_time)
                else:
                    # sorry bud, time's up
                    return data
            else:
                # status must be some manner of error
                logging.debug("Error status found in get_child for "+pk+"\n"
                              + "Status is "+status+"\n"
                              + json.dumps(data, indent=4, sort_keys=True))
                return data
        else:
            # Should I be throwing an exception here instead?
            logging.error("Status in get_child for "+pk+" was no retrievable")
            logging.error(json.dumps(data, indent=4, sort_keys=True))
    # We shouldn't get here
    logging.error("Error in get_child for \n"+pk+"\n No child retrievable")
    return None


def get_synonyms(curie):
    synonyms = []
    payload = {"curies": [curie]}
    r = requests.post(url=NORMALIZER_URL, data=json.dumps(payload), verify=False)
    rj = r.json()
    if keys_exist(rj, curie, "equivalent_identifiers"):
        for id in rj[curie]["equivalent_identifiers"]:
            synonyms.append(id["identifier"])
        return synonyms
    else:
        logging.warning("No synonyms were found for "+curie)
        return [curie]


@pytest.mark.asyncio
async def main():
    none_report_cards = await test_not_none()
    must_report_cards =await test_must_have_curie()
    # for report_card in none_report_cards:
    #     for agent,grade in report_card.items():
    #         assert grade == "Pass"
    # for report_card in must_report_cards:
    #     for agent,grade in report_card.items():
    #         assert grade == "Pass"


if __name__ == '__main__':
    asyncio.run(main())
