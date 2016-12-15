#! /usr/bin/env python

from distutils.core import setup

setup(name           = 'gzippy',
    version          = '0.1.2',
    description      = 'Gzip file utility.',
    url              = 'http://github.com/seomoz/gzippy',
    author           = 'Dan Lecocq',
    author_email     = 'dan@moz.com',
    packages = [
        'gzippy'
    ],
    package_dir = {
        'gzippy': 'gzippy'
    },
    install_requires = [
    ],
    tests_require    = [
        'coverage',
        'nose',
        'mock',
        'pylint',
        'rednose'
    ]
)
