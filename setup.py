from setuptools import setup

setup(
    name='Code Debt Metrics',
    version='0.1.1',
    packages=[
       'git_code_debt',
       'git_code_debt.metrics',
       'git_code_debt_server',
       'git_code_debt_server.logic',
       'git_code_debt_server.servlets',
       'git_code_debt_util',
    ],
    install_requires=[
        'flask',
        'mako',
        'simplejson',
    ],
)
