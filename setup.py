#! /usr/bin/env python3

from distutils.core import setup

setup(
    name             = 'gzippy',
    version          = '0.2.1',
    description      = 'Gzip file utility.',
    url              = 'http://github.com/seomoz/gzippy',
    author           = 'Pro Services',
    author_email     = 'turbo@moz.com',
    packages         = ['gzippy'],
    package_dir      = {'gzippy': 'gzippy'},
    install_requires = [],
    tests_require    = [
        'coverage',
        'nose',
        'mock',
        'pylint',
        'pycodestyle',
        'pydocstyle',
        'flake8'
        'rednose'
    ]
)
