from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='ImageProcessingServer',
      version=version,
      description="Easily stream OpenCV images to a server for heavy handling",
      long_description="""\
Want to offload image processing to a multithreaded multiprocess server? This is the library for you""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='OpenCV Server',
      author='Raaj',
      author_email='yaadhavraaj@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
