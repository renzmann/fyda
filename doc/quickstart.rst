.. _quickstart:

Quickstart
==========

.. contents:: Contents

Adding and loading data
-----------------------

Assuming installation went well, let's take some first steps using fyda with
your data. At its most basic level, fyda is a way to interface with your data.
By default, fyda will not have anything configured to work with it. Suppose
your project data lives in a folder named ~/myproject/input and has two data 
files inside it:

   #. 'example_data.csv' 
   #. 'some other data_with_A long NAME.xlsx'

The second file is particularly annoying, especially if you just want to
quickly call it up in a console or jupyter notebook. You could always hard
change the filename on your machine, but what if that file gets updated
automatically on a regular basis? Now it would be unreasonable to rename the
file every time. A simpler solution would be to use fyda's data configuration
to read your data automatically::

   >>> import fyda
   >>> fyda.set_data_root('~/myproject/input')
   >>> fyda.add_data('example', 'example.csv')
   >>> fyda.add_data('longname', 'some other data_with_A long NAME.xlsx')
   >>> quit()

Now fyda is ready to load up your data any time you import it into your project
sessions. It is **completely persistent**. Notice how we quit python above. If
we reboot python in the same environment, we can still load our data::

   >>> import fyda
   >>> example_data = fyda.load_data('example')

The :meth:`fyda.load_data` method is a flexible, smart data reader. It will
parse the filenames it was given when the data was added to figure out which
reader to use. 


A note on using excel files
---------------------------

If you are planning to use excel files like we did above, you may need to
configure some additional arguments. These additional configurations are key -
value pairs that will be passed to :meth:`pandas.read_excel`. 
