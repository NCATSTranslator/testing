"""Test ARS et all."""
import json
import os
from pathlib import Path
import urllib
import httpx
import pytest
import asyncio

#ARS_URL="https://ars.transltr.io/ars/api/"
ARS_URL="https://ars-dev.transltr.io/ars/api/"
BASE_PATH=os.path.dirname(os.path.realpath(__file__))

# with open("kps.json", "r") as stream:
#     KPS = json.load(stream)
# PAIRS = []
# for kp_name, url in KPS.items():
#     filename = Path("requests") / f"{kp_name}.json"
#     with open(filename, "r") as stream:
#         payload = json.load(stream)
#     PAIRS.append((kp_name, url, payload))




def get_files(relativePath):
    print("get_files")
    files=[]
    my_dir = BASE_PATH+relativePath
    for filename in os.listdir(my_dir):
        files.append(os.path.join(my_dir,filename))
    return files

async def test_not_none():
    print("test_not_none")
    files = get_files("/../ars-requests/not-none")
    for file in files:
        print("+++ Checking "+file)
        with open(file, "r") as f:
            query = json.load(f)
            await has_results(query)

async def call_ars(payload, url=ARS_URL+"submit"):
    print("call_ars")
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
    print("has_results")
    children = await get_children(query)
    for child in children:
        agent = child[0]
        childData=child[1]
        try:
            results = childData['fields']['data']['message']['results']
            if(not len(results)>0):
                print(agent +" has no results for \n")
                print(json.dumps(query, indent=4, sort_keys=True))
            else:
                print(agent +" has "+str(len(results))+" results")
        except (TypeError, KeyError) as e:
            print(agent +" has no results for \n")
            print(json.dumps(query, indent=4, sort_keys=True))


async def get_children(query,url=None):
    print("get_children")
    children = []
    response = await call_ars(query)
    pk = response['pk']
    if (url is None):
        url = ARS_URL+"messages/"+pk+"?trace=y"
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.get(
            url,
            timeout=10.0
        )
    data = r.json()
    for child in data['children']:
        agent = child['actor']['agent']
        childPk=child['message']
        childUrl=ARS_URL+"messages/"+childPk
        # with urllib.request.urlopen(ARS_URL+"messages/"+childPk) as url:
        #     childData = json.loads(url.read().decode())
        #     children.append(
        #         {agent,childData}
        #     )
        async with httpx.AsyncClient(verify=False) as client:
            childResponse = await client.get(
                childUrl,
                timeout=10.0
            )
            childData = childResponse.json()
            children.append(
                [agent,childData]
            )
    return children

@pytest.mark.asyncio
async def main():
    result = await test_not_none()

if __name__ == '__main__':
    asyncio.run(main())