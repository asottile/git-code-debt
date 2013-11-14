all: test itest

itests: itest
tests: test

test: py_env
	bash -c 'source py_env/bin/activate && \
		testify tests -x integration'

itest: py_env
	bash -c 'source py_env/bin/activate && \
		testify tests -i integration'

py_env: requirements.txt
	rm -rf py_env
	virtualenv py_env
	bash -c 'source py_env/bin/activate && \
		pip install -r requirements.txt'

clean:
	rm -rf py_env
