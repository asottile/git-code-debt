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
	cat schema/* | sqlite3 `python -c 'import git_code_debt_server.config; print git_code_debt_server.config.DATABASE_PATH'`
	bash -c 'source py_env/bin/activate && \
		PYTHONPATH=. python git_code_debt/populate_metric_ids.py'

py_env: requirements.txt
	rm -rf py_env
	virtualenv py_env
	bash -c 'source py_env/bin/activate && \
		pip install -r requirements.txt'

clean: clean_tables
	rm -rf py_env

clean_tables:
	rm -f `python -c 'import git_code_debt_server.config; print git_code_debt_server.config.DATABASE_PATH'`
