#!/usr/bin/env python

import os
import setuptools
import sys
import time

from pistonsupport import setuphelp as ps

INSTALL_DIR = os.path.join(sys.prefix, 'share', 'dashboard')
TOPDIR = os.path.abspath(os.path.dirname(__file__))
VFILE  = os.path.join(TOPDIR, 'version.py')

args = filter(lambda x: x[0] != '-', sys.argv)
command = args[1] if len(args) > 1 else ''

if command == 'sdist':
    PISTON_VERSION = os.environ['PISTON_VERSION']
    with file(VFILE, 'w') as f:
        f.write('''#!/usr/bin/env python\nVERSION = '%s'\n''' % PISTON_VERSION)
elif command == 'develop':
    PISTON_VERSION = time.strftime('9999.0.%Y%m%d%H%M%S', time.localtime())
    with file(VFILE, 'w') as f:
        f.write('''#!/usr/bin/env python\nVERSION = '%s'\n''' % PISTON_VERSION)
elif command is None:
    PISTON_VERSION = '9999999999-You_did_not_set_a_version'
else:
    assert os.path.exists(VFILE), 'version.py does not exist, please set PISTON_VERSION (or run make_version.py for dev purposes)'
    import version as pistonversion
    PISTON_VERSION = pistonversion.VERSION
    assert '9999.0' not in PISTON_VERSION, 'Please build this from a source tarball'

packages, data_files = ps.discover_things_in(TOPDIR, ['django-openstack', 'openstack-dashboard'])
data_files = ps.finish_for_setuptools(data_files, INSTALL_DIR)

setuptools.setup(
    name = 'dashboard',
    packages = packages,
    data_files = data_files,
    version = PISTON_VERSION,
    url = 'https://github.com/cloudbuilders/openstack-dashboard.git',
    license = 'Apache 2.0',
    description = "A Django interface for OpenStack.",
    author = 'Devin Carlen',
    author_email = 'devin.carlen@gmail.com',
    install_requires = ['setuptools', 'mox>=0.5.0'],
    zip_safe = False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
