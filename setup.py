from setuptools import find_packages
from setuptools import setup


setup(
    name='git_code_debt',
    description='A dashboard for monitoring code debt in a git repository.',
    url='https://github.com/Yelp/git-code-debt',
    version='0.8.0',

    author='Anthony Sottile',
    author_email='asottile@umich.edu',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    packages=find_packages('.', exclude=('tests*', 'testing*')),
    package_data={
        'git_code_debt': [
            'schema/*.sql',
        ],
        'git_code_debt.server': [
            'templates/*.mako',
            'static/css/*.css',
            'static/img/*.gif',
            'static/js/*.js',
            'metric_config.sample.yaml',
        ],
    },
    install_requires=[
        'flask',
        'jsonschema',
        'mako',
        'pyyaml',
        'PyStaticConfiguration[yaml]',
        'six',
    ],

    entry_points={
        'console_scripts': [
            'git-code-debt-create-tables = git_code_debt.create_tables:main',
            'git-code-debt-generate = git_code_debt.generate:main',
            'git-code-debt-list-metrics = git_code_debt.list_metrics:main',
            'git-code-debt-server = git_code_debt.server.app:main',
        ],
    },
)
