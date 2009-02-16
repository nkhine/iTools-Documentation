:mod:`itools.http` HTTP
***********************

.. module:: itools.http
   :synopsis: HTTP

.. index::
   single: HTTP

.. contents::


The package :mod:`itools.http` provides support for the HTTP protocol (see
RFC2616 for the specification). Basically it includes handlers for HTTP
requests and responses.

This is a low-level programming interface. For a high-level programming
interface to build web applications, see chapter :mod:`itools.web`.


The request
===========

A client, like a web browser, sends an HTTP request to the server.  An HTTP
request looks like this:

.. code-block:: none

    POST /;login HTTP/1.1
    Host: localhost:8080
    User-Agent: Mozilla/5.0
    Accept: text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5
    Accept-Language: es,en;q=0.8,fr;q=0.5,pt;q=0.3
    Accept-Encoding: gzip,deflate
    Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
    Keep-Alive: 300
    Connection: keep-alive
    Referer: http://localhost:8080/;login_form
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 34

    username=toto%40xxx.com&password=a

As you see it is basically a file, which is sent through the wire, from the
client to the server. It has a simple readable format, which consists of three
parts:

* The *request line*. It is the first line, and contains: the *request
  method*, the requested *uri* and the protocol version.
* The *headers*. Each line after the *request line*, and before the first
  blank line, is a *header*; where a *header* has a name and a value. Headers
  are used to information about the client (``User-Agent``, ``Agent``), about
  the connection (``Keep-Alive``, {``Connection``), etc.
* The *body*. At the end, separated from the *header* by a blank line, comes
  the body. It contains extra information, for example the values of a form,
  or a file that is uploaded. Most requests do not include a body.

To work with HTTP requests (and responses) :mod:`itools.http` offers a file
handler::

    >>> from itools.http import Request
    >>>
    >>> request = Request('request.txt')
    >>> request
    <itools.http.request.Request object at 0x2b59beffc6d8>
    >>>
    >>> print request.method
    POST
    >>> print request.request_uri
    /;login
    >>> print request.http_version
    HTTP/1.1
    >>> print request.get_header('user-agent')
    Mozilla/5.0

Here there is a summary of the programming interface of request objects (the
details can be found in the reference chapter):

.. class:: Request

  .. method:: set_header(name, value)

  .. method:: has_header(name)

  .. method:: get_header(name)

  .. method:: get_referrer()

  .. method:: get_parameter(name, default=None, type=None)

  .. method:: has_parameter(name)

  .. method:: set_cookie(name, value)

  .. method:: get_cookie(name)


The response
============

The Web server replies the client by sending an HTTP response. It looks like
this:

.. code-block:: none

    HTTP/1.1 200 OK
    Date: Fri, 22 Jun 2007 13:03:00 GMT
    Server: Apache
    Last-Modified: Fri, 22 Jun 2007 13:02:32 GMT
    ETag: "15c188-6-46b4ea00"
    Accept-Ranges: bytes
    Content-Length: 6
    Keep-Alive: timeout=15, max=100
    Connection: Keep-Alive
    Content-Type: text/plain

    Hello

Like the request, the response is split in three sections:

* The *status line*. It is the first line, and contains the protocol version,
  the *status code* and the *reason phrase*.
* The *headers*. Just like the request, the headers are a set of fields with a
  name and a value.
* The *body*. And at the end, the body.

To work with the HTTP responses we have a handler too::

    >>> from itools.http import Response
    >>>
    >>> response = Response('response.txt')
    >>> print response.status
    200
    >>> print response.get_content_length()
    6
    >>> print response.body
    Hello

And the programming interface:

.. class:: Response

  .. method:: set_header(name, value)

  .. method:: has_header(name)

  .. method:: get_header(name)

  .. method:: set_status(status)

  .. method:: get_status()

  .. method:: set_body(body)

  .. method:: redirect(location, status=302)

  .. method:: get_content\_length()

  .. method:: set_cookie(name, value, \*\*kw)

  .. method:: del_cookie(name)

  .. method:: get_cookie(name)
