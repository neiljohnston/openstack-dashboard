#!/usr/bin/env python

import os
import setuptools
import sys
import time

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

packages = setuptools.find_packages(where='django-openstack')

data_files = {}
for p in setuptools.findall('openstack-dashboard'):
    d, _ = os.path.split(p)
    full = os.path.join(INSTALL_DIR, d)
    data_files[full] = data_files.get(full, [])
    data_files[full].append(p)

setuptools.setup(
    name = 'dashboard',
    packages = packages,
    data_files = data_files.items(),
    package_dir = {
        'django_openstack': 'django-openstack/django_openstack',
    },
    package_data = {
        'django_openstack':
        [os.path.relpath(x, 'django-openstack/django_openstack/')
            for x in setuptools.findall('django-openstack/django_openstack/templates')],
    },
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
