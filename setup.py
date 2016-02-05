from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='fk-websocket-checker',
      version=version,
      description="Healthcheck for websockets.",
      long_description="""\
Validates if websockets endpoints are healthly.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Websocket HealthCheck',
      author='Gabriel Pereira',
      author_email='gabriellpweb@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'websocket',# -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
