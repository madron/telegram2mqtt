#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

from telegram2mqtt import version

file_name = os.path.join('requirements.txt')
with open(file_name, 'r') as r:
    requirements = [l for l in r.read().splitlines()]

setup(
    name='telegram2mqtt',
    version=version,
    description='Telegram to Mqtt gateway',

    author='Massimiliano Ravelli',
    author_email='massimiliano.ravelli@gmail.com',

    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: System :: Automation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='telegram mqtt',

    packages=find_packages(),
    install_requires=requirements,
    entry_points = dict(
        console_scripts=['telegram2mqtt=telegram2mqtt.__main__:main'],
    )
)
