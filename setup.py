"""
mgtoolkit: metagraph implementation tool

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2017, dinesha ranathunga.
Copyright 2023, Eric Parsonage.
Licensed under MIT.
"""
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as test_command

if sys.version_info[0] != 3  or sys.version_info[1] < 5:
    print("mgtoolkit requires Python  3.5, 3.6, 3.7, 3.8, 3.9, 3.10 or 3.11 (%d.%d detected)." %
          sys.version_info[0:2])
    sys.exit(-1)


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(test_command):
    # noinspection PyAttributeOutsideInit
    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [

]

# noinspection PyPep8
setup(
    name='mgtoolkit',
    version='1.1.3',
    description="This is a Python package for implementing metagraphs.",
    long_description=readme + '\n\n' + history,
    author="Eric Parsonage",
    author_email='eric@eparsonage.com',
    url='https://github.com/lamestllama/mgtoolkit',
    packages=[
        'mgtoolkit'
    ],
    package_dir={'mgtoolkit':
                 'mgtoolkit'},

    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Networking',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3.11',
        'Natural Language :: English'
    ],

    keywords="mgtoolkit, metagraph implementation, policy analysis",
    zip_safe=True,
    download_url = 'http://pypi.python.org/pypi/mgtoolkit',
    tests_require=['pytest'],

    entry_points={
        'console_scripts': [
            'mgtoolkit = mgtoolkit.console_script:console_entry',
        ],
    }

)
