"""Setup."""
from setuptools import setup


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='fyda',
    packages=['fyda'],
    version='0.4.4',
    license='MIT',
    description='General data interface for Python 3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Robert Enzmann',
    author_email='runningwithrobb@gmail.com',
    url='https://github.com/renzmann/fyda',
    keywords=['Python', 'Data', 'Interface', 'Data Science', 'python 3'],
    install_requires=[
        'numpy',
        'pandas',
        'configparser',
        'boto3',
        'pyyaml',
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
