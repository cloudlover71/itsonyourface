#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
  name='emf_sdk',
  version='0.1.1',
  description='Expedia EMF SDK',
  package_dir={'emf_sdk': 'emf_sdk'},
  packages=['emf_sdk', 'emf_sdk/senders'],
  install_requires=['fluent-logger'],
  author='Trofim Prodayvoda',
  author_email='t.prodayvoda@gmail.com',
  url='https://github.com/radiusinc/Expedia-EMF-SDK',
  download_url='',
  license=''
)
