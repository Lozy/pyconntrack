#!/usr/bin/env python
from setuptools import setup

setup(
    name='pyconntrack',
    version='1.0.1-beta',
    description='nf_conntrack api',
    url='https://github.com/Lozy/pyconntrack',
    author='Konia Zheng',
    author_email='konia@maxln.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='nf_conntrack wrapper for python',
    packages=['pyconntrack']
)
