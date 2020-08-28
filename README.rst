mongo2md: a command-line tool for MongoDB documentation generation
################################################

mongo2md  is a command line tool for MongoDB documentation generation
It generates mock files from Mongo database, allows you to add comments and builds Markdown files


.. contents::

.. section-numbering::



Main features
=============

* Database schema identification
* Mock files generation
* Build-in Markdown generation
* Low memory footprint
* Documentation
* Test coverage



Installation
============


macOS
-----


On macOS, undatum can be installed via `Homebrew <https://brew.sh/>`_
(recommended):

.. code-block:: bash

    $ brew install mongo2md


A MacPorts *port* is also available:

.. code-block:: bash

    $ port install mongo2md

Linux
-----

Most Linux distributions provide a package that can be installed using the
system package manager, for example:

.. code-block:: bash

    # Debian, Ubuntu, etc.
    $ apt install mongo2md

.. code-block:: bash

    # Fedora
    $ dnf install mongo2md

.. code-block:: bash

    # CentOS, RHEL, ...
    $ yum install mongo2md

.. code-block:: bash

    # Arch Linux
    $ pacman -S mongo2md


Windows, etc.
-------------

A universal installation method (that works on Windows, Mac OS X, Linux, …,
and always provides the latest version) is to use pip:


.. code-block:: bash

    # Make sure we have an up-to-date version of pip and setuptools:
    $ pip install --upgrade pip setuptools

    $ pip install --upgrade mongo2md


(If ``pip`` installation fails for some reason, you can try
``easy_install mongo2md`` as a fallback.)


Python version
--------------

Python version 3.6 or greater is required.



Usage
=====


Synopsis:

.. code-block:: bash

    $ mongo2md [flags] prepare dbname [collname]

.. code-block:: bash
    $ mongo2md [flags] document projpath

See also ``mongo2md --help``.


How to use
----------
1. Run `mongo2md prepare` command with selected database
2. Go to the directory with generated files
3. Edit '*_fields.csv' and 'tables.csv' files, add "displayName" and "description" fields. Make sure to use utf -8
4. Run `python -m mongo2md document` will generate Markdown files for

Examples
--------

Build mock files from 'budgetreg' database with 'budgetreg' collection and store to 'projects/budgetreg' directory

.. code-block:: bash

    $ mongo2md prepare --output projects/budgetreg budgetreg budgetreg


Builds markdown

.. code-block:: bash

    $ mongo2md document projects/budgetreg
