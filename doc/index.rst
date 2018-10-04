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

.. contents:: Table of Contents

.. highlight:: none

Installation
------------
It is recommended that you use the Anaconda distribution of Python 3 with
ifydat. It is also recommended that you have a separate virtual environment (if
you haven't made one already).


Assuming your current working directory is where you want to put this repo,:: 

   $ git clone https://github.com/renzmann/ifydat


Next, install the requirements

(Linux / macOS)::

   $ while read requirement; do conda install --yes $requirement; done < requirements.txt

(Windows)::

   > FOR /F "delims=~" %f in (requirements.txt) DO conda install --yes "%f" || pip install "%f"

Finally, install fyda::

   $ pip install .



User Guide
----------

See the :ref:`quickstart` to quickly get started using fyda.

Working with configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   ProjectConfig
   add_data
   remove_data
   add_directory
   remove_directory
   set_data_root


Loading configured data
~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   load_data


.. _under-construction:

Under Construction
------------------

Quickstart guide
~~~~~~~~~~~~~~~~

   - :ref:`quickstart`

Data shaping
~~~~~~~~~~~~

   - basic pipelines

Modeling
~~~~~~~~

   - model selection
   - model training
   - model tuning and support


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
