"""Test services under failure conditions."""
import json
import os

import httpx
import pytest

with open("services.json", "r") as stream:
    SERVICES = json.load(stream)
PAIRS = [tuple(pair) for pair in SERVICES.items()]


async def call_service(url, data):
    """Call a service."""
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            url,
            headers=headers,
            data=data,
            timeout=30.0,
        )
    return response.status_code, response.text


@pytest.mark.parametrize("service_name,url", PAIRS)
@pytest.mark.asyncio
async def test_invalid_json(service_name, url):
    """Test invalid JSON."""
    data = "{"
    status_code, text = await call_service(url, data)
    os.makedirs("results/invalid_json", exist_ok=True)
    with open(f"results/invalid_json/{service_name}_{status_code}.txt", "w") as stream:
        stream.write(text)
    assert status_code in (400, 422)
    assert "json" in text.lower()


@pytest.mark.parametrize("service_name,url", PAIRS)
@pytest.mark.asyncio
async def test_invalid_trapi(service_name, url):
    """Test invalid TRAPI."""
    data = json.dumps({"message": "uh oh"})
    status_code, text = await call_service(url, data)
    os.makedirs("results/invalid_trapi", exist_ok=True)
    with open(f"results/invalid_trapi/{service_name}_{status_code}.txt", "w") as stream:
        stream.write(text)
    assert status_code in (400, 422)
    assert "message" in text.lower()


@pytest.mark.parametrize("service_name,url", PAIRS)
@pytest.mark.asyncio
async def test_broken_edge(service_name, url):
    """Test broken edge."""
    data = json.dumps({"message": {"query_graph": {
        "nodes": {
            "n0": {
                "ids": ["MONDO:0005737"]
            },
            "n1": {}
        },
        "edges": {
            "e01": {
                "subject": "uh oh",
                "object": "n1",
            }
        }
    }}})
    status_code, text = await call_service(url, data)
    os.makedirs("results/broken_edge", exist_ok=True)
    with open(f"results/broken_edge/{service_name}_{status_code}.txt", "w") as stream:
        stream.write(text)
    assert status_code in (400, 422)


@pytest.mark.parametrize("service_name,url", PAIRS)
@pytest.mark.asyncio
async def test_bad_predicate(service_name, url):
    """Test bad predicate."""
    data = json.dumps({"message": {"query_graph": {
        "nodes": {
            "n0": {
                "ids": ["MONDO:0005737"],
                "categories": ["biolink:Disease"]
            },
            "n1": {
                "categories": ["biolink:ChemicalSubstance"]
            }
        },
        "edges": {
            "e01": {
                "subject": "n0",
                "object": "n1",
                "predicates": ["biolink:treats"]
            }
        }
    }}})
    status_code, text = await call_service(url, data)
    os.makedirs("results/bad_predicate", exist_ok=True)
    with open(f"results/bad_predicate/{service_name}_{status_code}.txt", "w") as stream:
        stream.write(text)
    assert status_code == 200


@pytest.mark.parametrize("service_name,url", PAIRS)
@pytest.mark.asyncio
async def test_no_such_data(service_name, url):
    """Test no such data."""
    data = json.dumps({"message": {"query_graph": {
        "nodes": {
            "n0": {
                "ids": ["MONDO:XXX"],
                "categories": ["biolink:Disease"]
            },
            "n1": {
                "categories": ["biolink:ChemicalSubstance"]
            }
        },
        "edges": {
            "e01": {
                "subject": "n1",
                "object": "n0",
                "predicates": ["biolink:treats"]
            }
        }
    }}})
    status_code, text = await call_service(url, data)
    os.makedirs("results/no_such_data", exist_ok=True)
    with open(f"results/no_such_data/{service_name}_{status_code}.txt", "w") as stream:
        stream.write(text)
    assert status_code == 200
