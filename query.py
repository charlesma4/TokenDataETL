from constants import (
	GRAPH_TIMEOUT,
	GRAPH_API_URL
)

import requests

query = f'''{{
    token(id: "0x3472a5a71965499acd81997a54bba8d852c6e53d"){{
        name
        symbol
        totalLiquidity
    }}
}}'''

r = requests.post(GRAPH_API_URL, json={'query': query}, timeout=GRAPH_TIMEOUT)

print(r.json())
