# TokenDataETL
ETL to pull token data

## Setup Instructions
`git clone git@github.com:charlesma4/TokenDataETL.git`

If you don't have the `requests` and `psycopg2` packages, install them with:
- `pip3 install requests`
- `pip3 install psycopg2-binary`

For unit testing, you'll also need to install the `mock` package:
- `pip3 install mock`

To store our data, you need to spin up a Postgresql database instance. This is easy with [homebrew](https://docs.brew.sh/Installation) (for Mac users):
1. `brew update && brew doctor` (homebrew health check)
1. `brew install postgresql`
1. `brew services start postgresql`

You can verify that the above has worked by running `psql` to access your database via the terminal.

Lastly, create a a database titled `test`, or whatever name you prefer (make sure to change the code in loader.py if you want a different DB name).
From your terminal, after starting postgresql as explained above, run:
1. `psql`
1. `create database test;`

Take note of the user that appears before the `=#` in your psql prompt - you'll need to use that user in loader.py, when establishing the db connection.

Now, to run the app, from the root directory, you can execute:
`python3 src/token_metric_etl/app.py --token-id <token-id-1 here> --token-id <token-id-2 here> --volume --liquidity`

If you'd like to verify functionality with unit tests, run:
`python3 test/test_main.py`

