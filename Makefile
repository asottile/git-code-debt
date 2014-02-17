
TEST_TARGETS =
ITEST_TARGETS = -m integration
UTEST_TARGETS = -m "not(integration)"

all: _tests

integration:
	$(eval TEST_TARGETS := $(ITEST_TARGETS))

unit:
	$(eval TEST_TARGETS := $(UTEST_TARGETS))

utests: test
utest: test
tests: test
test: unit _tests
itests: itest
itest: integration _tests

_tests: py_env
	bash -c 'source py_env/bin/activate && py.test tests $(TEST_TARGETS)'

ucoverage: unit coverage
icoverage: integration coverage

coverage: py_env
	bash -c 'source py_env/bin/activate && \
		coverage erase && \
		coverage run `which py.test` tests $(TEST_TARGETS) && \
		coverage report -m'

tables: py_env clean_tables
	bash -c 'source py_env/bin/activate && \
		python -m git_code_debt.create_tables ./database.db'

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
