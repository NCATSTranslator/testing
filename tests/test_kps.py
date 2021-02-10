"""Test KPs."""
import json
import os
from pathlib import Path

import httpx
import pytest

with open("kps.json", "r") as stream:
    KPS = json.load(stream)
PAIRS = []
for kp_name, url in KPS.items():
    filename = Path("requests") / f"{kp_name}.json"
    with open(filename, "r") as stream:
        payload = json.load(stream)
    PAIRS.append((kp_name, url, payload))


async def call_kp(url, payload):
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            url,
            json=payload,
            timeout=30.0,
        )
    response.raise_for_status()
    return response.json()


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
