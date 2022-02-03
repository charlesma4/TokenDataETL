from extract.data_sources.uniswap_v2 import UniswapV2
from transform.transformer import Transform
from load.loader import Loader
import argparse
import time


def run():
	# constant - should be moved to another constants file - mapping of data needed for a metric to metric name
	metric_data_pairings = {
		"volume": "swaps",
		"liquidity": "liquidity"
	}

	parser = argparse.ArgumentParser(description="Start ETL service for token data.")
	parser.add_argument("--token-id", action="append", type=str,
                    	help="a token ID to load metrics for")
	for metric in metric_data_pairings:
		parser.add_argument("--" + metric, action="store_true", help="Load {} data".format(metric))
	args = parser.parse_args()

	tokens_to_queries = {token: [] for token in args.token_id}
	args_dict = vars(args)
	for arg in args_dict:
		if arg == "token_id":
			continue

		if args_dict[arg]:
			for token in tokens_to_queries:
				tokens_to_queries[token].append(metric_data_pairings[arg])

	uniswap_source = UniswapV2(tokens_to_queries)
	# if there are multiple data sources for same token, add additional aggregation step
	# in case of volume/liquidity, can just sum everything together for a given token_id
	transformer = Transform(args_dict)
	loader = Loader()

	while True:
		tokens_to_data = uniswap_source.run_extraction()
		tokens_to_metrics = transformer.run_transformation(tokens_to_data)
		loader.run_load(tokens_to_metrics)
		print("Successfully loaded these metrics:", tokens_to_metrics)
		time.sleep(60)

if __name__ == "__main__":
	run()