#!/usr/bin/env python
# -*- coding: utf-8 -

import os
import sys

if not hasattr(sys, 'version_info') or sys.version_info < (2, 5, 0, 'final'):
    raise SystemExit("oauth client requires Python 2.5 or later.")

from setuptools import setup, find_packages
from oauthclient import __version__
 
setup(
    name = 'django-oauthclient',
    version = __version__,
    description = 'A tree-legged oauth authentication application for django',
    long_description = file(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author = 'Alexis Metaireau',
    author_email = 'ametaireau@gmail.com',
    license = 'BSD',
    url = 'http://bitbucket.org/bisonvert/django-oauthclient',
    install_requires = [
            "Django >= 1.1",
    ]
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages = find_packages(),

    # Make setuptools include all data files under version control,
    # svn and CVS by default
    include_package_data=True,
    zip_safe=False,
    # Tells setuptools to download setuptools_git before running setup.py so
    # it can find the data files under Hg version control.
    setup_requires=['setuptools_hg'],
)
