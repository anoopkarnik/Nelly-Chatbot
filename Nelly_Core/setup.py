#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import datetime
import sys

from setuptools import setup, find_packages

BUILD = ''  # test by setting to ".dev0" if multiple in one day, use ".dev1", ...
DATE = datetime.date.today().isoformat().replace('-', '')

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python >=3.6 is required for Nelly.')

with open('README.md', encoding="utf8") as f:
    # strip the header and badges etc
    readme = f.read().split('--------------------')[-1]

with open('requirements.txt') as f:
    reqs = []
    for line in f:
        line = line.strip()
        reqs.append(line.split('==')[0])


if __name__ == '__main__':
    setup(
        name='Nelly core',
        version='0.1.{DATE}{BUILD}'.format(DATE=DATE, BUILD=BUILD),
        description='Life long AI councelor',
        long_description=readme,
        long_description_content_type='text/markdown',
        url='www.NervPlus.com',
        python_requires='>=3.6',
        # packages=find_packages(
        #     exclude=('data', 'docs', 'examples', 'tests',)
        # ),
        install_requires=reqs,
        include_package_data=True,
        package_data={'': ['*.txt', '*.md']},
        entry_points={
            "flake8.extension": ["PAI = core.utils.flake8:ParlAIChecker"],
            "console_scripts": ["parlai=parlai.__main__:main"],
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Natural Language :: English",
        ],
    )
