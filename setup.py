# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='currency',
    version='0.1.0',
    description='Currency converter',
    long_description=readme,
    author='Pavol Vargovčík',
    author_email='pavol.vargovcik@gmail.com',
    url='https://github.com/p4l1ly/currency',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'currency': ['symbols.html']},
    scripts=['scripts/currency_converter.py']
)
