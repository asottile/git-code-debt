
all: tables test itest

itests: itest
tests: test

test: py_env
	bash -c 'source py_env/bin/activate && \
		testify tests -x integration'

itest: py_env
	bash -c 'source py_env/bin/activate && \
		testify tests -i integration'

tables: py_env clean_tables
	bash -c 'source py_env/bin/activate && \
		PYTHONPATH=. python git_code_debt/schema.py ./database.db && \
		PYTHONPATH=. python git_code_debt/populate_metric_ids.py ./database.db'

py_env: requirements.txt
	rm -rf py_env
	virtualenv py_env
	bash -c 'source py_env/bin/activate && \
		pip install -r requirements.txt'

start:
	bash -c 'source py_env/bin/activate && \
		PYTHONPATH=. python -m git_code_debt_server.app ./database.db'

clean: clean_tables
	rm -rf py_env

clean_tables:
	rm -f ./database.db
