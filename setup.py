"""Setup."""
from setuptools import setup

setup(
  name = 'fyda',
  packages = ['fyda'],
  version = '0.1',
  license='MIT',
  description = 'General data interface for Python 3',
  author = 'Robert Enzmann',
  author_email = 'runningwithrobb@gmail.com',
  url = 'https://github.com/renzmann/fyda',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['Python', 'Data', 'Interface', 'Data Science', 'python 3'],
  install_requires=[
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
