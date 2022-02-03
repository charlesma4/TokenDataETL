create_token_metrics_table = """
	CREATE TABLE IF NOT EXISTS token_metrics (
		token_id VARCHAR(64) NOT NULL,
		token_name VARCHAR(128) NOT NULL,
		volume FLOAT,
		liquidity FLOAT,
		year INTEGER NOT NULL,
		month INTEGER NOT NULL,
		day INTEGER NOT NULL,
		hour INTEGER NOT NULL,
		unix_time BIGINT NOT NULL
	);
"""

insert_token_metrics = """
	INSERT INTO token_metrics (
		token_id,
		token_name,
		volume,
		liquidity,
		year,
		month,
		day,
		hour,
		unix_time
	) VALUES (
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s
	)
"""