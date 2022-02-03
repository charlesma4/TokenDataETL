import sys
sys.path.append("../src")

from token_metric_etl.extract.data_sources import uniswap_v2
import unittest
import mock
import time

pairs_query_response = {
    'data': {
        'pairs': [{
            'id': '0x00000',
            'reserveUSD': '1000',
            'token0': {'name': 'MemeCoin'}
        }]
    }
}

swaps_query_response = {
    'data': {
        'swaps': [
            {'amountUSD': '100'},
            {'amountUSD': '100'}
        ]
    }
}

mints_query_response = {
    'data': {
        'mints': [
            {'amountUSD': '200'},
            {'amountUSD': '100'}
        ]
    }
}

burns_query_response = {
    'data': {
        'burns': [
            {'amountUSD': '500'},
            {'amountUSD': '100'}
        ]
    }
}

# This method will be used by the mock to replace requests.get
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2':
        if "pairs" in kwargs["json"]["query"]:
            return MockResponse(pairs_query_response, 200)
        elif "swaps" in kwargs["json"]["query"]:
            return MockResponse(swaps_query_response, 200)
        elif "mints" in kwargs["json"]["query"]:
            return MockResponse(mints_query_response, 200)
        elif "burns" in kwargs["json"]["query"]:
            return MockResponse(burns_query_response, 200)


    return MockResponse(None, 404)

class TestUniswapV2(unittest.TestCase):
    @mock.patch("requests.post", side_effect=mocked_requests_post)
    def test_init(self, mock_post):
        tokens_to_queries = {
            "0x00000": ["swaps", "liquidity"]
        }
        data_source = uniswap_v2.UniswapV2(tokens_to_queries)
        assert data_source.tokens_to_pairs == {("0x00000", "MemeCoin"): ["0x00000", "0x00000"]}
        assert data_source.tokens_to_liquidity == {("0x00000", "MemeCoin"): 2000.0}

    @mock.patch("requests.post", side_effect=mocked_requests_post)
    @mock.patch("token_metric_etl.extract.data_sources.uniswap_v2.time", return_value=1000)
    def test_run_extraction(self, mock_post, mock_time):
        tokens_to_queries = {
            "0x00000": ["swaps", "liquidity"]
        }
        data_source = uniswap_v2.UniswapV2(tokens_to_queries)
        tokens_to_data = data_source.run_extraction()
        assert tokens_to_data == {
            ('0x00000', 'MemeCoin'): {
                'swaps': [100.0, 100.0],
                'mints': [200.0, 100.0],
                'burns': [500.0, 100.0],
                'timestamp': 1000,
                'liquidity': 1700.0
            }
        }

if __name__ == '__main__':
    unittest.main()
