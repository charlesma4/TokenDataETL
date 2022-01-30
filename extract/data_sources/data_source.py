"""
An interface for writing DataSource classes
"""
class DataSource:
	def __init__(self):
		pass

	def request(self, query):
		pass

	def parse(self, raw_data):
		pass
