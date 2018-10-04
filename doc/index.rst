.. ifydat documentation master file, created by
   sphinx-quickstart on Mon Oct  1 10:21:24 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: fyda

fyda: An interface "For Your DAta"
====================================

fyda is a data interface designed for use with Python data science projects.

Here's how it works:
 
   * You have a project *in its own virtual environment*
   * You install ``fyda`` into this virtual environment
   * You configure ``fyda`` to open, read, write, model and be merry with your
     data
   * Your code becomes 1000x smaller and more readable.

.. warning::
   This project is still under construction.
   See the :ref:`under-construction` section for what is to come.

.. toctree::
   :maxdepth: 2

   quickstart
   userguide

.. contents:: Table of Contents

.. highlight:: none

Installation
------------
It is recommended that you use the Anaconda distribution of Python 3 with
fyda. It is also recommended that you have a separate virtual environment (if
you haven't made one already).


Assuming your current working directory is where you want to put this repo,:: 

   $ git clone https://github.com/renzmann/fyda


Next, install the requirements

(Linux / macOS)::

   $ while read requirement; do conda install --yes $requirement; done < requirements.txt

(Windows)::

   > FOR /F "delims=~" %f in (requirements.txt) DO conda install --yes "%f" || pip install "%f"

Finally, install fyda::

   $ pip install .



.. _under-construction:

Under Construction
------------------

There are many, many features we would like to implement into fyda. Here are
some of the top priorities:

Connecting to SQL
~~~~~~~~~~~~~~~~~

This would be a huge time saver and is the most needed portion of fyda.

Data shaping
~~~~~~~~~~~~

fyda should have some form of handling data pipelines and transformation
scripts.

Modeling
~~~~~~~~

A stretch goal would be to give fyda some of these powers (in cooperation with
sklearn):

   - model selection
   - model training
   - model tuning and support


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
