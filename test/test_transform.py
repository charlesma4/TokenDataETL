import sys
sys.path.append("../src")

from token_metric_etl.transform import transformer
import unittest

class TestTransformer(unittest.TestCase):
    def test_run_transformation(self):
        tokens_to_data = {
            ('0x00000', 'MemeCoin'): {
                'swaps': [100.0, 100.0],
                'mints': [200.0, 100.0],
                'burns': [500.0, 100.0],
                'timestamp': 1000,
                'liquidity': 1700.0
            }
        }
        args_dict = {
            'token_id': ['0x3472a5a71965499acd81997a54bba8d852c6e53d'],
            'volume': True,
            'liquidity': True
        }
        transformer_test = transformer.Transformer(args_dict)
        tokens_to_metrics = transformer_test.run_transformation(tokens_to_data)
        assert tokens_to_metrics == {
            ('0x00000', 'MemeCoin'): {
                'timestamp': 1000,
                'liquidity': 1700.0,
                'volume': 200.0
            }
        }


if __name__ == '__main__':
    unittest.main()
