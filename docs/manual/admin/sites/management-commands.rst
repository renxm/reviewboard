.. _management-commands:

============================
Advanced Management Commands
============================

:command:`rb-site` provides a ``manage`` command for certain management tasks.
The format for the commands is always::

    $ rb-site manage /path/to/site command-name -- parameters


The management commands that administrators are most likely to use are
explained in detail in the following sections.

To get a complete list of all management commands, run::

    $ rb-site manage /path/to/site help

And to retrieve information on a specific management command::

    $ rb-site manage /path/to/site help command-name


.. _search-indexing:

Search Indexing
---------------

Review Board installations with indexed search enabled must periodically
index the database. This is done through the ``rebuild_index`` and
``update_index`` management commands (The ``index`` command will be
deprecated in a future release).

To perform an index update::

    $ rb-site manage /path/to/site update_index


To perform a full index::

    $ rb-site manage /path/to/site rebuild_index


These commands should be run periodically in a task scheduler, such as
:command:`cron` on Linux. It is advisable to update the index
roughly every 10 minutes, and a full index once a week during off-peak
hours.

A sample ``crontab`` entry is available at :file:`conf/search-cron.conf` under
an installed site directory.

The generated search index will be placed in the
:ref:`search index directory <search-index-directory>` specified in the
:ref:`general-settings` page. By default, this should be the
:file:`search-index` directory in your site directory.


.. _creating-a-super-user:

Creating a Super User
---------------------

It is possible to create a new super user account without using the
website. This can be important if the main super user account is for
whatever reason disabled or if the login information is lost.

To create a new super user account, run::

    $ rb-site manage /path/to/site createsuperuser


This will prompt for the username and password of the account. You must
specify a user that doesn't already exist in the database. Once this is
finished, you should be able to log in under the new account and fix any
problems you have.


Opening a Command Shell
-----------------------

Power users who wish to run Python commands against an installed Review
Board server can do so with the ``shell`` management command. This can be
useful if you're a developer looking to test some code against Review
Board.

To open a Python command shell, run::

    $ rb-site manage /path/to/site shell


Resetting Review Request Counters
---------------------------------

The counters in the Dashboard along the left-hand side, indicating the
number of review requests, can potentially be incorrect if changes were
made manually to the database or if there was an error while attempting to
save information to the database.

You can fix these counters by running::

    $ rb-site manage /path/to/site fixreviewcounts

This is done automatically when upgrading a site.
