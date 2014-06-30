from setuptools import find_packages
from setuptools import setup

setup(
    name='git_code_debt',
    version='0.3.4',
    packages=find_packages('.', exclude=('tests*', 'testing*')),
    package_data={
        'git_code_debt': [
            'schema/*.sql',
        ],
        'git_code_debt_server': [
            'templates/*.mako',
            'static/css/*.css',
            'static/js/*.js',
        ],
    },
    install_requires=[
        'argparse',
        'flask',
        'mako',
        'PyStaticConfiguration',
        # TODO: remove pyyaml when PyStaticConfiguration supports [yaml]
        'pyyaml',
        'simplejson',
    ],
)
