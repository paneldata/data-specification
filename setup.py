#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

requirements = ["click>=7.0", "dpath", "goodtables>=2.0", "pyyaml>=5.0"]

setup(
    author="Heinz-Alexander Fuetterer",
    entry_points={
        "console_scripts": ["ddionrails-datapackage=ddionrails_datapackage.cli:cli"]
    },
    install_requires=requirements,
    include_package_data=True,
    name="ddionrails_datapackage",
    packages=find_packages(),
    package_data={
        "ddionrails_datapackage": ["datapackage/*.yml", "datapackage/*/*.yml"]
    },
    version="0.1.0",
    zip_safe=False,
)
