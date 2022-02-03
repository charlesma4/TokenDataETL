from .data_source import DataSource
import requests
import json
from time import time

class UniswapV2(DataSource):
	api_url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
	api_timeout = 10
	queries = {
		"swaps": '''{{
		    swaps(where: {{pair_in: {pair_ids}, timestamp_gt: {} }}) {{
		        amountUSD
		    }}
		}}''',
		"mints": '''{{
			mints(where:{{pair_in: {pair_ids}, timestamp_gt: {}}}) {{
				amountUSD
			}}
		}}''',
		"burns": '''{{
			burns(where:{{pair_in: {pair_ids}, timestamp_gt: {}}}) {{
				amountUSD
			}}
		}}
		'''
		}

	pair_id_queries = [
	'''
		{{  
			pairs (where :{{token0 : "{token_id}", volumeUSD_gt: 0}}) {{
			    id
			    token0 {{
			    	name
			    }}
			    reserveUSD
			}}
		}}
	''',
	'''
		{{  
			pairs (where :{{token1 : "{token_id}", volumeUSD_gt: 0}}) {{
			    id
			    token1 {{
			    	name
			    }}
			    reserveUSD
			}}
		}}
	'''
	]

	"""
	@param tokens_to_queries: dictionary of token_id: [query_key] mappings
	"""
	def __init__(self, tokens):
		self.tokens_to_pairs = {}
		self.tokens_to_liquidity = {}
		for token in tokens:
			# find pair IDs based on requested token
			# needed to query for swaps on that pair
			formatted_pair_query_0 = self.pair_id_queries[0].format(token_id=token)
			formatted_pair_query_1 = self.pair_id_queries[1].format(token_id=token)

			pair_ids = []

			pair_data_0 = self.request(formatted_pair_query_0)["pairs"]
			pair_data_1 = self.request(formatted_pair_query_1)["pairs"]
			total_liq = 0
			for entry in pair_data_0:
				pair_ids.append(entry["id"])
				total_liq += float(entry["reserveUSD"])
			for entry in pair_data_1:
				pair_ids.append(entry["id"])
				total_liq += float(entry["reserveUSD"])

			try:
				token_key = (token, pair_data_0[0]["token0"]["name"])
			except:
				try:
					token_key = (token, pair_data_1[0]["token0"]["name"])
				except Exception as e:
					print("No pairs exist for the given token {}, skipping.".format(token))
					continue

			self.tokens_to_pairs[token_key] = pair_ids
			self.tokens_to_liquidity[token_key] = total_liq

	def request(self, query):
		res = requests.post(self.api_url, json={"query": query}, timeout=self.api_timeout)
		return res.json()["data"]

	def parse_swaps(self, raw_data):
		return [float(swap["amountUSD"]) for swap in raw_data["swaps"]]

	def parse_mints(self, raw_data):
		return [float(mint["amountUSD"]) for mint in raw_data["mints"]]

	def parse_burns(self, raw_data):
		return [float(burn["amountUSD"]) for burn in raw_data["burns"]]

	def run_extraction(self):
		token_to_data = {}
		for token in self.tokens_to_pairs:
			data_points = {}
			pair_ids = self.tokens_to_pairs[token]
			curr_time = int(time())
			for query in self.queries:
				query_time = curr_time - 86400 if query == "swaps" else curr_time - 60
				raw_data = self.request(self.queries[query].format(query_time, pair_ids=json.dumps(pair_ids)))
				if query == "swaps":
					parsed_data = self.parse_swaps(raw_data)
				elif query == "mints":
					parsed_data = self.parse_mints(raw_data)
				elif query == "burns":
					parsed_data = self.parse_burns(raw_data)

				data_points[query] = parsed_data

			data_points["timestamp"] = curr_time

			# liquidity is calculated in data source due to immediate availability
			data_points["liquidity"] = self.tokens_to_liquidity[token] + sum(data_points["mints"]) - sum(data_points["burns"])
			self.tokens_to_liquidity[token] = data_points["liquidity"]
			token_to_data[token] = data_points
		return token_to_data
