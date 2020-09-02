# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in rama_aluminium/__init__.py
from rama_aluminium import __version__ as version

setup(
	name='rama_aluminium',
	version=version,
	description='Customization for Aluminium Product Manufacturing Company',
	author='GreyCube Technologies',
	author_email='admin@greycube.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
