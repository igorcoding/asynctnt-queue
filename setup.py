# -*- coding: utf-8 -*-
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

description = "Tarantool Queue python/asyncio bindings"
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = description


def find_version():
    for line in open("asynctnt_queue/__init__.py"):
        if line.startswith("__version__"):
            return re.match(
                r"""__version__\s*=\s*(['"])([^'"]+)\1""", line).group(2)


setup(
    name="asynctnt-queue",
    packages=["asynctnt_queue"],
    include_package_data=True,
    version=find_version(),
    author="igorcoding",
    author_email="igorcoding@gmail.com",
    url='https://github.com/igorcoding/asynctnt-queue',
    license='Apache Software License',
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Front-Ends"
    ],
    install_requires=[
        'asynctnt>=0.1.8'
    ],
    description=description,
    long_description=long_description,
    test_suite='run_tests.discover_tests'
)
