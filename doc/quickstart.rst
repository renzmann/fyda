.. _quickstart:

Quickstart
==========

.. contents:: Contents

Loading Data
------------

At its most basic level, fyda is a way to interface with your data.
The objective is to make loading and saving your data files easy and intuitive.
fyda achieves this with two simple concepts:

   #. A file called ``.fydarc`` that has manually configured values.
   #. "Shortcuts" that uniquely map to your data files.

Wherever your data is stored, fyda will assume that it all lies under some
root directory, which should be the first thing specified in .fydarc::

   [directories]
   root = ~/myproject/data

Let's suppose that the ``myproject`` folder has the following structure::

   .
   ├── data
   │  ├── arrays
   │  │   ├── X.npy
   │  │   └── y.npy
   │  └── raw
   │      ├── transactions.pickle
   │      ├── consumers.csv
   │      └── external.xlsx
   └ .fydarc

and that the contents of ``.fydarc`` are as above. Normally when loading
the data files into python, you need to open the correct reader and point
to the raw string location for that file. fyda takes care of this with
a recursive search through the root folder and automatic shortcut naming
and reader assignment. Using fyda from a python shell running in
``~/myproject`` would look like this::

   >>> import fyda
   >>> transactions = fyda.load('transactions')
   >>> X = fyda.load('X')
   >>> y = fyda.load('y')
   ...
   >>> external = fyda.load('external')

And that's it! By removing the raw string references, the code becomes
more extensible and scalable. The recommended way to use fyda with your
projects is for each system to have its own .fydarc located at the
directory where python is executed from. This .fydarc should **not** be
pushed to the master branch of the repository, but instead maintained
locally. You can also manually tell your script where the .fydarc it
should use is located by setting ``fyda.options.CONFIG_LOCATION`` option
to the full filepath of .fydarc.

You can also manually specify shortcuts in .fydarc by creating a section
called ``[data]`` organized as::

   [data]
   <shortcut 1> = <relative file location to root>
   ...
   <shortcut n> = <relative file location to root>

This is particularly useful when the original file names are very long 
and the default shortcut assignment would be cumbersome to use, or when 
solving duplcate file name issues (more on this below).


Using fyda to get file paths
----------------------------

When working with data on multiple platforms, it can be a pain to make sure all
of the references to data locations are consistent. Once the "input_folder" is
set for fyda, telling the code where to find it is easy. Using the example
data we added earlier, it would look like this::

   >>> fyda.data_path('example')
   '/home/username/myproject/input/example.csv'

If you use the same code on a Windows machine, it would instead return::

   >>> fyda.data_path('example')
   'C:\\Users\\username\\myproject\\input\\example.csv'

This is useful when collaborating on a project or when you need platform
independence for your code.


How fyda handles duplicate names
--------------------------------

There are some situations that can cause namespace issues with the shortcut
method above:

   #. A folder contains two files with the same prefix, but different file
      extensions.
   #. Two or more folders have unique file names (prefix + extension) within
      themselves, but file names are not pairwise disjoint across combinations
      of folders.
   #. A combination of both situations above.

fyda's method of solving this is by first adding on file extensions to the
shortcuts of the duplicate offenders and seeing if that fixes the issue.
If not, it will start adding on the containing folders' names to the
shortcuts until uniqueness is achieved. As an example, consider the
following situation::

   .
   ├── data
   │  ├── arrays
   │  │   ├── X.npy
   │  │   └── y.npy
   │  └── raw
   │      ├── X.csv
   │      └── y.pickle
   └ .fydarc

In this case, the prefix for X and y is not unique across folders, so fyda
needs to resolve the duplicate name issue. fyda first tries adding the
file extensions, and since this leads to a unique namespace, it stops
there::

   >>> X_arr = fyda.load('X.npy')
   >>> y_arr = fyda.load('y.npy')
   >>> X_raw = fyda.load('X.csv')
   >>> y_raw = fyda.load('y.pickle')

Keep in mind that you can always specify specific shortcut assignments in the
``[data]`` section of your .fydarc; for example, if your fydarc looks like 
this::

   [directories]
   root = ~/myproject/data

   [data]
   X = raw/X.csv
   y = raw/y.pickle

Then fyda will keep the shortcuts you assigned, but reassign any others that
it finds::

   >>> X_arr = fyda.load('X.npy')
   >>> y_arr = fyda.load('y.npy')
   >>> X_raw = fyda.load('X')
   >>> y_raw = fyda.load('y')

To complicate matters further, what if we now had a file structure like this::

   .
   ├── data
   │  ├── arrays
   │  │   ├── X.csv
   │  │   └── y.npy
   │  └── raw
   │      ├── X.csv
   │      └── y.pickle
   └ .fydarc

Now the ``X`` data file has the same name in both folders, so just adding the
extension won't do. Now, fyda has to add the containing folders' names to gain
uniqueness::

   >>> X_arr = fyda.load('arrays/X.csv')
   >>> y_arr = fyda.load('y.npy')
   >>> X_raw = fyda.load('raw/X.csv')
   >>> y_raw = fyda.load('y.pickle')

Note that the ``y`` files are still only separated by file extensions.


Peeking under the hood: the DataBank
------------------------------------

Connecting to and using fyda with Amazon S3
-------------------------------------------

