import sys
sys.path.append("../src")

from token_metric_etl.load import loader
import unittest
import mock

class TestLoader(unittest.TestCase):
    @mock.patch("token_metric_etl.load.loader.psycopg2.connect")
    def test_run_load(self, mock_connection):
        tokens_to_metrics = {
            ('0x00000', 'MemeCoin'): {
                'timestamp': 1000,
                'liquidity': 1700.0,
                'volume': 200.0
            }
        }

        mock_conn = mock_connection.return_value
        mock_cur = mock_conn.cursor.return_value


        loader_test = loader.Loader()
        loader_test.run_load(tokens_to_metrics)
        assert mock_cur.execute.called
        assert mock_conn.commit.called


if __name__ == '__main__':
    unittest.main()
