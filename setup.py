#!/usr/bin/env python

from setuptools import setup

setup(name='pybitset',
      version='0.1',
      description='A simple library to manage bitsets.',
      author='Shashank Shanbhag',
      author_email='shashank@shashtag.net',
      license='MIT License',
      url='https://github.com/essessv',
      packages=['pybitset'],
      tests_require=['nose'],
      extras_require={
          'testing': ['nose'],
      },
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 3 - Alpha',
          'Natural Language :: English',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      )
