from setuptools import find_packages
from setuptools import setup

setup(
    name='Code Debt Metrics',
    version='0.1.3',
    packages=find_packages('.', exclude=('tests*', 'testing*')),
    package_data={
        'git_code_debt_server': [
            'templates/*',
            'static/css/*',
            'static/js/*',
        ],
    },
    install_requires=[
        'flask',
        'mako',
        'simplejson',
    ],
)
