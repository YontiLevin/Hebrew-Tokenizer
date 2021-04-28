#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from io import open
from setuptools import setup, find_packages


# Package meta-data.
NAME = "hebrew_tokenizer"
DESCRIPTION = "A very simple python tokenizer for Hebrew text"
URL = "https://github.com/yontilevin/hebrew_tokenizer"
EMAIL = "therealyontilevin@gmail.com"
AUTHOR = "Yonti Levin"
VERSION = "2.1.0"

# with open("README.md", "r", encoding='utf8') as fh:
#     long_description = fh.read()
long_description = """
go to github for more info
"""
here = os.path.abspath(os.path.dirname(__file__))

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        # Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
    ],
)
