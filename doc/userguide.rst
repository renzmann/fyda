.. _userguide:


==============
fyda API Guide
==============

Loading Data
------------

.. currentmodule:: fyda

.. autofunction:: load

.. autofunction:: load_s3

.. autofunction:: data_path


DataBank
--------

.. autoclass:: fyda.DataBank

Properties
~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   DataBank.tree
   DataBank.shortcuts
   DataBank.readers

Methods
~~~~~~~

.. autosummary::
   :toctree: generated/

   DataBank.deposit
   DataBank.determine_shortcut
   DataBank.encoding_level
   DataBank.rebase_shortcuts
   DataBank.root_to_dict
   DataBank.withdraw


ProjectConfig
-------------

.. autoclass:: fyda.ProjectConfig
