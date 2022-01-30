from data_source import DataSource
import requests
import json
from time import time

class UniswapV2(DataSource):
	api_url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
	api_timeout = 10
	queries = {
		"swaps": '''{{
		    swaps(where: {{pair_in: {pair_ids}, timestamp_gt: {day_ago} }}) {{
		        id
		        amountUSD
		    }}
		}}'''
	}

	pair_id_query = '''
		{{  
			pairs (where :{{token0 : "{token_id}", volumeUSD_gt: 0}}) {{
			    id
			}}
		}}
	'''

	"""
	@param tokens_to_queries: dictionary of token_id: [query_key] mappings
	"""
	def __init__(self, tokens_to_queries):
		self.tokens_to_queries = {}
		for token in tokens_to_queries:
			# find pair IDs to based on requested token
			# needed to query for swaps on that pair
			formatted_query = self.pair_id_query.format(token_id=token)
			pair_ids = []
			for entry in self.request(formatted_query)["pairs"]:
				pair_ids.append(entry["id"])
			self.tokens_to_queries[token] = {}
			for query in tokens_to_queries[token]:
				self.tokens_to_queries[token][query] = self.queries[query].format(pair_ids=json.dumps(pair_ids), day_ago=int(time() - 86400))


	def request(self, query):
		res = requests.post(self.api_url, json={"query": query}, timeout=self.api_timeout)
		return res.json()["data"]

	def parse_swaps(self, raw_data):
		return [swap["amountUSD"] for swap in raw_data["swaps"]]

	def run_extraction(self):
		token_to_data = {}
		for token in self.tokens_to_queries:
			for query in self.tokens_to_queries[token]:
				raw_data = self.request(self.tokens_to_queries[token][query])
				parsed_swaps = self.parse_swaps(raw_data)
				self.tokens_to_queries[token][query] = parsed_swaps
				
		return self.tokens_to_queries

