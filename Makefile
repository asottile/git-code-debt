
all: tables test itest

itests: itest
tests: test

test: py_env
	bash -c 'source py_env/bin/activate && \
		testify tests -x integration'

itest: py_env
	bash -c 'source py_env/bin/activate && \
		testify tests -i integration'

coverage: py_env
	bash -c 'source py_env/bin/activate && \
		coverage erase && \
		coverage run `which testify` tests && \
		coverage combine && \
		coverage report -m --omit="/usr/*,py_env/*,*/__init__.py,tests/*,pre-commit.py,*_mako"'

tables: py_env clean_tables
	bash -c 'source py_env/bin/activate && \
		PYTHONPATH=. python -m git_code_debt.create_tables ./database.db'

start: py_env
	bash -c 'source py_env/bin/activate && \
		PYTHONPATH=. python -m git_code_debt_server.app ./database.db'

py_env: requirements.txt
	rm -rf py_env
	virtualenv py_env
	bash -c 'source py_env/bin/activate && \
		pip install -r requirements.txt'

clean: clean_tables
	rm -rf py_env

clean_tables:
	rm -f ./database.db
