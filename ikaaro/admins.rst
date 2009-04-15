Administrators Guide
####################

.. contents::

.. highlight:: sh

Introduction
============

.. _admins-requirements:

Requirements
------------

Python 2.5.2 and :mod:`itools` [#admins-itools]_ 0.60 are required. It is
recommended to install the :mod:`pil` [#admins-pil]_ and :mod:`docutils`
[#admins-docutils]_ packages.

To be able to index office documents (ODF, PDF, etc.) the libraries :mod:`wv2`
[#admins-wv2]_ and :mod:`poppler` [#admins-poppler]_  are needed.


Download and Install
--------------------

Download the latest :mod:`ikaaro` version from http://www.hforge.org/ikaaro.
Then to install it just type::

    $ tar xzf ikaaro-X.Y.Z.tar.gz
    $ cd ikaaro-X.Y.Z
    $ ipkg-build.py
    $ python setup.py install


The command line interface
--------------------------

The :mod:`ikaaro` package includes a collection of command line tools to
create and manage instances:

    ============================== ===============================================
    :file:`icms-init.py`           creates a new :mod:`ikaaro` instance
    ------------------------------ -----------------------------------------------
    :file:`icms-start.py`          starts the web and the mail spool servers
    ------------------------------ -----------------------------------------------
    :file:`icms-stop.py`           stops the both servers
    ------------------------------ -----------------------------------------------
    :file:`icms-update.py`         updates the instance (after a software upgrade)
    ------------------------------ -----------------------------------------------
    :file:`icms-update-catalog.py` rebuilds the catalog
    ============================== ===============================================



All the scripts are self-documented, just run any of them with the ``--help``
option.  This is an excerpt for the :file:`icms-init.py` script::

    $ icms-init.py --help
    Usage: icms-init.py [OPTIONS] TARGET

    Creates a new instance of ikaaro with the name TARGET.

    Options:
      --version             show program's version number and
                            exit
      -h, --help            show this help message and exit
      -a ADDRESS, --address=ADDRESS
                            listen to IP ADDRESS
      -e EMAIL, --email=EMAIL
                            e-mail address of the admin user
      -p PORT, --port=PORT  listen to PORT number
      -r ROOT, --root=ROOT  create an instance of the ROOT
                            application
      -s SMTP_HOST, --smtp-host=SMTP_HOST
                            use the given SMTP_HOST to send
                            emails
      -w PASSWORD, --password=PASSWORD
                            use the given PASSWORD for the
                            admin user


Make a new instance
===================

To create a new instance we use the :file:`icms-init.py` script. Example::

    $ icms-init.py --email=jdavid@itaapy.com my_instance
    *
    * Welcome to ikaaro
    * A user with administration rights has been created for you:
    *   username: jdavid@itaapy.com
    *   password: 7WEBJr
    *
    * To start the new instance type:
    *   icms-start.py my_instance
    *

(Take note of the automatically generated password, you will need it to enter
the application through the web interface.)

The :file:`icms-init.py` script creates a folder (named :file:`my_instance` in
the example) that keeps, among other things, the database and a configuration
file::

    $ tree -F -L 1 --noreport my_instance
    my_instance
    |-- catalog/
    |-- config.conf
    |-- database/
    |-- log/
    `-- spool/


.. _admins-configuration-file:

The configuration file
----------------------

Once the instance is created, it is a good idea to read the self-documented
configuration file, :file:`config.conf`, to learn about the available options,
and to finish the configuration process.

The different options can be split in four groups:

* The ``modules`` option allows to load (import) the specified Python packages
  when the server starts. This is the way we can extend the :mod:`ikaaro` CMS
  with third party packages.
* The ``address`` and ``port`` options define the internet address and the
  port number the Web server will listen to.

  By default connections are accepted from any internet address. In a
  production environment it is wise to restrict the connections to only those
  comming from the localhost. Section :ref:`admins-production` explains the
  details.
* The ``smtp-host``, ``smtp-login`` and ``smtp-password`` are used to define
  the SMTP relay server that is to be used to send emails; and to provide the
  credentials for servers that require authentication.

  The ``contact-email`` option must be a valid email address, it will be used
  for the ``From`` field in outgoing messages.

  It is very important to set these options to proper values, since the
  :mod:`ikaaro` CMS sends emails for several important purposes.
* The ``debug`` option if set will output extra informations to the events
  log, the ``log/events`` file.


Start/Stop the server
=====================

The :mod:`ikaaro` CMS can be started simply be the use of the
:file:`icms-start.py` script::

    $ icms-start.py my_instance
    [my_instance] Web Server listens *:8080

By default the process remain attached to the console, to stop it just
type ``Ctrl+C``.  It is stopped ``gracefully``, what means that pending
requests will be handled and the proper responses sent to the clients.

To detach from the console use the ``--detach`` option. Then, to stop the
servers started this way use the :file:`icms-stop.py` script::

    $ icms-start.py --detach my_instance
    ...
    $ icms-stop.py my_instance
    [my_instance] Web Server shutting down (gracefully)...

With the Web server running, we can open our favourite browser and go to the
``http://localhost:8080`` URL, to reach the user interface (see figure).

.. figure:: figures/back-office.*
   :align: center

   The :mod:`ikaaro` Web interface.


A look inside
=============

The content of an :mod:`ikaaro` instance is:

* The configuration file (see section :ref:`admins-configuration-file`).
* The logs folder (see below).
* The database (see below).
* The catalog keeps the indexes needed to quickly search in the database.
* The mail spool keeps the emails to be sent by the spool server.


The logs
--------

There are four log files:

* The access log uses the *Common Log Format* [#admins-logs]_, useful for
  example to build statistics about the usage of the web site.
* By default the events log keeps record of the database transactions.  In
  debug mode (see section :ref:`admins-configuration-file`), more low-level
  information is recorded. This log file contains also information about every
  *internal server* error, specifically the request headers and the Python
  tracebacks.
* The spool log keeps track of the emails sent by the spool server.
* The spool error log keeps information about every error coming from the
  spool server.


The database
------------

The data is stored directly in the file system. This is what a new instance
looks like::

    $ tree --noreport -F my_instance/database
    my_instance/database
    |-- .metadata
    |-- users/
    |   `-- 0.metadata
    `-- users.metadata

The database is made up of regular files and folders. For instance, a Web Page
will be stored in the database as an XHTML file, an image or an office
document will be stored as it is.

This is extremely useful for introspection and manipulation purposes, since we
can use the old good Unix tools: ``grep``, ``vi``, etc. But of course, *don't
make any changes unless you know what you are doing!*


Metadata
^^^^^^^^

Every :mod:`ikaaro` object is defined by a metadata file. As the example
shows, a new instance has three objects: the root (defined by the
:file:`.metadata` file), the users folder, and the admin user created by the
init script.

A metadata file looks like this:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <metadata format="user" version="20071215">
      <password>FNp6/Vb9cFeAMTlQNcFylixbToQ%3D%0A</password>
      <email>jdavid@itaapy.com</email>
    </metadata>


.. _admins-production:

Deployment in a production environment
======================================

In a production environment it is highly recommended to deploy :mod:`ikaaro`
behind Apache [#admins-apache]_, using it as a proxy. The rewrite rule cannot
be simpler:

.. code-block:: apache

  <VirtualHost *:80>
    ServerName example.com
    RewriteEngine On
    RewriteRule ^/(.*) http://localhost:8080/$1 [P]
  </VirtualHost>

To finish, the configuration of the :mod:`ikaaro` server should restrict (for
security reasons) the internet addresses it accepts connections from to the
localhost:

    ``address = 127.0.0.1``


Virtual Hosts
-------------

Most of the setup required for virtual hosting is defined in the :mod:`ikaaro`
side, and through the Web interface. Regarding the rewrite rule the only thing
needed is to add as many *aliases* as virtual hosts, for example:

.. code-block:: apache

  <VirtualHost *:80>
    ServerName example.com
    ServerAlias vhost1.example.com
    ServerAlias vhost2.example.com
    RewriteEngine On
    RewriteRule ^/(.*) http://localhost:8080/$1 [P]
  </VirtualHost>


Upgrading to a new software version
===================================

Generally major versions of :mod:`ikaaro` include changes to the layout or to
the format of the information stored in the database that require an upgrade.

The update process has two steps::

    # 1. Update the database
    $ icms-update.py --yes my_instance
    ...
    # 2. Rebuild the catalog
    $ icms-update-catalog.py --yes my_instance
    ...

Anyway, any major version of :mod:`ikaaro` includes upgrade notes that detail
any particular procedure.  Start a version upgrade by reading these notes.


Recovering from a crash
=======================

Though unlikely, it may happen that the server crashes leaving a transaction
in the middle, for example, if there is a power failure at the bad time. If
this happens, the server will refuse to start again, but it must provide some
instructions to restore the database (``git`` commands).


.. rubric:: Footnotes

.. [#admins-itools]  http://www.hforge.org/itools

.. [#admins-pil] http://www.pythonware.com/products/pil/

.. [#admins-docutils] http://docutils.sourceforge.net

.. [#admins-wv2] http://sourceforge.net/projects/wvware/

.. [#admins-poppler] http://poppler.freedesktop.org/

.. [#admins-logs] http://www.w3.org/Daemon/User/Config/Logging.html\#common-logfile-format

.. [#admins-apache] http://http.apache.org

