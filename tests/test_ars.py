"""Test ARS et all."""
import json
import os
from pathlib import Path
import urllib
import httpx
import pytest

ARS_URL="https://ars.transltr.io/ars/api/"
# with open("kps.json", "r") as stream:
#     KPS = json.load(stream)
# PAIRS = []
# for kp_name, url in KPS.items():
#     filename = Path("requests") / f"{kp_name}.json"
#     with open(filename, "r") as stream:
#         payload = json.load(stream)
#     PAIRS.append((kp_name, url, payload))

def main():
    pass

if __name__ == '__main__':
    main()


def open_files(relativePath):
    for filename in os.listdir(os.getcwd()):
        with open(os.path.join(os.getcwd(),filename),'r') as f:
            pass

async def call_ars(payload, url=ARS_URL+"submit"):
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            url,
            json=payload,
            timeout=60.0,
        )
    response.raise_for_status()
    return response.json()


async def must_contain_curie(curie,query):
    results = get_children(query)

async def has_results(query):
    children = get_children(query)
    for k, v in children:
        results = v['fields']['data']['message']['results']
        if(len(results)>0):
            pass
        else:
            print(k+" has no results for \n")
            print(print(json.dumps(json.loads(query), indent=4, sort_keys=True)))

async def get_children(query,url=None):
    children = []
    response = call_ars(query)
    pk = response['pk']
    with urllib.request.urlopen(ARS_URL+"messages/"+pk+"?trace=y") as url:
        data = json.loads(url.read().decode())
    for child in data['children']:
        agent = child['actor']['agent']
        childPk=child['message']
        with urllib.request.urlopen(ARS_URL+"messages/"+childPk) as url:
            childData = json.loads(url.read().decode())
            children.append(
                {agent,childData}
            )
    return children


@pytest.mark.parametrize("kp_name,url,payload", PAIRS)
@pytest.mark.asyncio
async def test_one_hop(kp_name, url, payload):
    """Test one-hop queries."""
    response_json = await call_kp(url, payload)

    responses_path = Path("responses")
    responses_path.mkdir(parents=True, exist_ok=True)
    filename = responses_path / f"{kp_name}.json"
    with open(filename, "w") as stream:
        json.dump(response_json, stream, indent=4)
