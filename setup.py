#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Template used:
# https://github.com/kennethreitz/setup.py

from setuptools import find_packages, setup

NAME = "ddionrails_datapackage"
DESCRIPTION = "Build and validate Tabular Data Packages for ddionrails studies"
URL = "https://github.com/paneldata/data-specification"
EMAIL = "hfuetterer@diw.de"
AUTHOR = "Heinz-Alexander Fütterer"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.2.0"
KEYWORDS = ["datapackage", "paneldata", "ddionrails", "data-validation", "jsonschema"]
LICENSE = "BSD 3-Clause"
CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation :: CPython",
]

REQUIRED = [
    "click>=7.0",
    "dpath",
    "goodtables>=2.0",
    "python-frontmatter",
    "pyyaml>=5.0",
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests"]),
    package_data={
        "ddionrails_datapackage": ["datapackage/*.yml", "datapackage/resources/*.yml"]
    },
    entry_points={
        "console_scripts": ["ddionrails-datapackage=ddionrails_datapackage.cli:cli"]
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license=LICENSE,
    keywords=KEYWORDS,
    classifiers=CLASSIFIERS,
)
