import psycopg2
from datetime import datetime
from .query import create_token_metrics_table, insert_token_metrics

class Loader:
	def __init__(self):
		self.conn = self.establish_db_connection()
		self.cur = self.conn.cursor()
		self.create_table()


	def create_table(self):
		self.cur.execute(create_token_metrics_table)
		self.conn.commit()

	def establish_db_connection(self, db="test", user="charlesma"):
		try:
			conn = psycopg2.connect(database=db,
									user=user)
		except Exception as e:
			print("Failed to establish database connection: {}".format(e))
			raise

		return conn

	def convert_timestamp(self, timestamp):
		metric_time = datetime.utcfromtimestamp(timestamp)
		return metric_time.year, metric_time.month, metric_time.day, metric_time.hour

	def run_load(self, tokens_to_metrics):
		for token in tokens_to_metrics:
			token_id, token_name = token[0], token[1]
			token_metrics = tokens_to_metrics[token]

			unix_timestamp = token_metrics["timestamp"]
			# timestamp conversion
			year, month, day, hour = self.convert_timestamp(unix_timestamp)

			self.cur.execute(insert_token_metrics, (
							 token_id,
							 token_name,
							 token_metrics["volume"],
							 token_metrics["liquidity"],
							 year,
							 month,
							 day,
							 hour,
							 unix_timestamp))

		self.conn.commit()
