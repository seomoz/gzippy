#! /usr/bin/env python

from distutils.core import setup

setup(name           = 'gzippy',
    version          = '0.1.1',
    description      = 'Gzip file utility.',
    url              = 'http://github.com/seomoz/gzippy',
    author           = 'Dan Lecocq',
    author_email     = 'dan@moz.com',
    py_modules = [
        'gzippy'
    ],
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
