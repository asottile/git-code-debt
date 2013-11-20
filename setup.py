from setuptools import find_packages
from setuptools import setup

setup(
    name='Code Debt Metrics',
    version='0.1.3',
    packages=find_packages('.', exclude=('tests*', 'testing*')),
    install_requires=[
        'flask',
        'mako',
        'simplejson',
    ],
)
