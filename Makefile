all: test

tests: test

test: py_env
	bash -c 'source py_env/bin/activate && \
		testify tests'

py_env: requirements.txt
	rm -rf py_env
	virtualenv py_env
	bash -c 'source py_env/bin/activate && \
		pip install -r requirements.txt'

clean:
	rm -rf py_env
