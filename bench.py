#! /usr/bin/env python

from __future__ import print_function

import gzip
import time

import gzippy


def timer(name, runs=1):
    '''Yield run times, collecting timing information.'''
    print(name)
    print('=' * len(name))

    times = []
    for run in range(runs):
        start = -time.time()
        yield run
        start += time.time()
        times.append(start)

    print('Average of %s runs: %s\n' % (runs, sum(times) / len(times)))


split = ['This is some example content'] * 100000
joined = '\n'.join(split)

for _ in timer('Gzip single write', 5):
    with gzip.open('example.gz', 'wb') as fout:
        fout.write(joined)

for _ in timer('Gzippy single write', 5):
    with gzippy.open('example.gz', 'wb') as fout:
        fout.write(joined)

for _ in timer('Gzip with repeated writes', 5):
    with gzip.open('example.gz', 'wb') as fout:
        for element in split:
            fout.write(element)

for _ in timer('Gzip with repeated writes', 5):
    with gzippy.open('example.gz', 'wb') as fout:
        for element in split:
            fout.write(element)

# Read in an example file
with gzip.open('example.gz', 'wb') as fout:
    fout.write(joined)

for _ in timer('Gzip with single read', 5):
    with gzip.open('example.gz', 'rb') as fin:
        fin.read()

for _ in timer('Gzippy with single read', 5):
    with gzippy.open('example.gz', 'rb') as fin:
        fin.read()

for _ in timer('Gzip iterlines', 5):
    with gzip.open('example.gz', 'rb') as fin:
        list(fin)

for _ in timer('Gzippy iterlines', 5):
    with gzippy.open('example.gz', 'rb') as fin:
        list(fin)
