:mod:`itools.http` HTTP
***********************

.. module:: itools.http
   :synopsis: HTTP

.. index::
   single: HTTP

.. contents::

The :mod:`itools.http` package offers an HTTP server with a simple programming
interface. It builds on the HTTP server provided by the `libsoup
<http://live.gnome.org/LibSoup>`_ C library (which is wrapped by the
:mod:`itools.soup` package).

.. note::

   This is a low-level programming interface. For a high-level web framework
   see the :mod:`itools.web` package.

Example:

.. code-block:: python

   from itools.http import HTTPServer

   class Ping(HTTPServer):
       def path_callback(self, soup_message, path):
           method = soup_message.get_method()
           body = '%s %s' % (method, path)
           soup_message.set_status(200)
           soup_message.set_response('text/plain', body)

   server = Ping()
   server.start()

