.. _quickstart:

Quickstart
==========

.. contents:: Contents

Adding and loading data
-----------------------

At its most basic level, fyda is a way to interface with your data.
By default, fyda will not have anything configured to work with it; you will
need to configure fyda in a python session or write a python script that adds
your desired configurations. Suppose
your project data lives in a folder named ~/myproject/input and has two data 
files inside it:

   #. 'example_data.csv' 
   #. 'some other data_with_A long NAME.xlsx'

The second file is particularly annoying, especially if you just want to
quickly call it up in a console or jupyter notebook. You could always hard
change the filename on your machine, but what if that file gets updated
automatically on a regular basis? Or if someone else has that file name
hard-coded? A simple solution would be to use fyda's data configuration
to read your data automatically::

   >>> import fyda
   >>> fyda.set_data_root('~/myproject/input')
   >>> fyda.add_data(example='example.csv',
   ...               longname='some other data_with_A long NAME.xlsx')
   >>> quit()

That's it. fyda is now ready to load up your data any time you import it into
your project sessions. It is **completely persistent**. Notice how we quit
python above. If we reboot python in the same environment, we can still load
our data::

   >>> import fyda
   >>> example_data = fyda.load_data('example')

The :meth:`fyda.load_data` method is a flexible, smart data reader. It will
parse the filenames it was given when the data was added to figure out which
reader to use. 

Inspecting your configuration
-----------------------------

If for any reason you need to manually edit your config file, you can find
its location using ``fyda.configurate.CONF_PATH``. However, it is better
advised to simply use fyda's builtin tools for viewing and editing the
configuration. To see what is configured in a section, simply pass the name of
that configuration section to :meth:`fyda.summary`::

   >>> fyda.summary('data')

   [data]
   example = example.csv
   longname = 'some other data_with_A long NAME.xlsx'

To see which sections are available in the configuration::

   >>> fyda.sections()
   ['directories', 'data', 'shortcut_map']

The ``'shortcut_map'`` is a special section used for reverse-mapping the
filenames back to the shortcuts, and generally you don't need to worry about
it, since fyda will handle all of that in the background.


Removing configurations
-----------------------

Let's say our ``example.csv`` is no longer useful or needed in the project.
Removing it from the configuration is as simple as::

   >>> fyda.remove_data('example')
   Section "data", option "example" sucessfully removed.

The way the response was worded here implies that there is some additional
options to removing and reconfiguring. Indeed, we can tell fyda to change, add,
or remove any section or option the same way that a normal
:class:`configparser.ConfigParser` would::

   >>> fyda.add_options('new_section', key='value')
   >>> fyda.summary('new_section')
   
   [new_section]
   key = value

We can also tell fyda to remove this in one of two ways; if you just want to
delete the key-value pair, but keep the section::

   >>> fyda.remove_options('new_section', 'key')
   Section "new_section", option "key" sucessfully removed.
   >>> fyda.summary('new_section')

   [new_section]

To remove this section altogether, use :meth:`fyda.remove_section`::

   >>> fyda.remove_section('new_section')
   Section "new_section" sucessfully removed.
