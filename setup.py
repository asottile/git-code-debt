from setuptools import find_packages
from setuptools import setup

setup(
    name='Code Debt Metrics',
    version='0.3.2',
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
        'flask',
        'mako',
        'simplejson',
    ],
)
