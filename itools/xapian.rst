:mod:`itools.xapian` Xapian
***************************

.. module:: itools.xapian
   :synopsis: A catalog based on Xapian

.. index:: Xapian

.. contents::


Python developers have a choice between two different solutions for searching
and indexing:

* Xapian [#xapian-xapian]_ is an Index & Search engine written in C++ and
  published with the GPL license. It includes a Python wrapper.
* Lucene [#xapian-lucene]_ is an Index & Search engine written in Java, and
  part of the Apache [#xapian-apache]_ project. It can be used from Python
  through the PyLucene wrapper [#xapian-pylucene]_.

Because Xapian is a powerful but very low-level engine we chose to add it a
layer to provide a powerful, but user friendly solution. We can access it
through the :mod:`itools.xapian` module.

The main advantage of :mod:`itools.xapian` is that it is by far the easiest
solution to learn and to use.


.. _xapian-quick-start:

Quick Start
===========

To illustrate the usage of :mod:`itools.xapian`, we are going to index and
search the Web! I mean, a couple of pages.


Create a new catalog
--------------------

.. function:: make_catalog(uri, fields)

    To create a new (and empty) catalog we use this function::

        >>> from itools.xapian import make_catalog
        >>>
        >>> catalog = make_catalog('catalog_test')

    The parameter is the path where the catalog will be created.  The value
    returned by :func:`make_catalog` is a catalog object, which offers an API
    for indexing, unindexing and searching.


Define the objects to be indexed
--------------------------------

.. class:: CatalogAware

    Objects to be indexed must inherit from the base class
    :class:`CatalogAware`, and implement the two methods
    :meth:`get\_catalog\_fields` and :meth:`get\_catalog\_values`:

        >>> from itools.xapian import CatalogAware
        >>> from itools.xapian import KeywordField, TextField
        >>> from itools.html import HTMLFile
        >>>
        >>> class Document(CatalogAware, HTMLFile):
        ...     def get_catalog_fields(self):
        ...         return [KeywordField('url', is_stored=True),
        ...                 TextField('body')]
        ...     def get_catalog_values(self):
        ...         return {'url': str(self.uri), 'body': self.to_text()}
        ...


Index
-----

Now we are going to index a couple of web pages::

    >>>
    # Load support for the HTTP protocol
    >>> import itools.http
    >>>
    # Index a couple of web pages
    >>> for url in ['http://www.python.org', 'http://git.or.cz/']:
    ...     document = Document(url)
    ...     catalog.index_document(document)
    ...
    # Save changes
    >>> catalog.save_changes()

Note that all changes are made in memory, and not saved to the file system
until the call to :meth:`save_changes` is made.


Search
------

Time to search::

    >>> results = catalog.search(body='python')
    >>> for document in results.get_documents():
    ...     print document.url
    ...
    http://www.python.org
    >>>


Building and Loading: the Constructors
======================================

In the :ref:`xapian-quick-start` we have seen the function
:func:`make_catalog`, which creates a new catalog in the file system.

We also need to see how to load a catalog that already exists, that was
created some time before. This is done using directly the class
:class:`Catalog`:

.. class:: Catalog

::

    >>> from itools.xapian import Catalog
    >>>
    >>> catalog = Catalog('catalog_test')

This call expects the file system path where the catalog was created.

Just to summarize these are the ways to build and to load, respectively,
a catalog object:

* :func:`make_catalog(path)`

    Creates a new and empty catalog at the given path.  Returns a catalog
    object (instance of the :class:`Catalog` class).
* :class:`Catalog(path)`

    Loads the catalog at the given path.

The fields to be indexed are defined by the indexed objects.  This we will see
in the next section.


Catalog Aware objects
=====================

Objects to be indexed must inherit from the base class :class:`CatalogAware`,
and implement the two methods :func:`get_catalog_fields` and
:func:`get_catalog_values`:

.. class: CatalogAware

    .. method:: get_catalog_fields()

        Returns a list with the definition of the fields to be indexed.  Each
        item of the list is a field, section :ref:`xapian-fields` explains the
        details.

    .. method:: get_catalog_values()

        Returns a dictionary with the field values for this instance. The
        dictionary maps field names to field values.


.. _xapian-fields:

Fields
======

The method :meth:`get_catalog_fields` defines the fields to index.

One thing we must choose when defining a field is its type. There are four
built-in types to choose from (it is also possible to define custom field
types, as we will see later):

* *TextField* This field type allows for full-text indexing. What means that
  the given text will be split into words, so it will be possible to search
  for individual words, or for phrases.
* *KeywordField* This type of field will index the value as it is, without any
  particular processing. This is useful for example to search fields whose
  values belong to a defined set of possible values (like an enumerate).
* *BoolField* This type of field is for boolean values (True or False).
* *IntegerField* This one is for integers.

Let's see again the fields definition of our example::

    def get_catalog_fields(self):
        return [KeywordField('url', is_stored=True),
                TextField('body')]

Other than the field type, we must define the name of the field, in this
example ``url`` and ``body``. As it's easy to guess we will use the field name
to make reference to it, when indexing and searching.

And finally, a field may be indexed and/or stored [#xapian-rq]_.


Indexed and Stored fields
-------------------------

If we choose to define a field as indexed (the default), we will be able to
search for it later.

If we choose to define a field as stored, we will be able to retrieve its
value from the catalog, without the need to load the original document; think
of it as a cache. By default a field is not stored.

For example, when indexing office documents, we will want to be able to search
their content, but we should not store it, because that would take too much
resources. However we may like to store some metadata, like the author and the
title, so we can show this information to the user without loading the
original document, hence speeding up the interface.

So the decision to index and/or store a field depends on the usage (no sense
to index a field if we are not going to search for it), and on performance
considerations.

.. _xapian-external-id:

The external id (and how to un-index a document)
------------------------------------------------

The first field in the definition (*url* in our example) is a special field:
it defines the *external id*. That is, the value that uniquely identifies the
original document, and that can be used to load it.

This first field must be both *indexed* and *stored*, and should probably be
of the type *KeywordField*.

Internally the catalog only uses the external identifier when unindexing
documents. The method :meth:`unindex_document` expects as parameter an
external id value, for example::

    >>>
    # Un-index
    >>> catalog.unindex_document('http://www.python.org')
    # Test
    >>> results = catalog.search(body='python')
    >>> for document in results.get_documents():
    ...     print document.url
    ...
    >>>


Howto define custom field types
-------------------------------

To define your own field type, you must create a new class that inherits from
:class:`BaseField`. :class:`BaseField` provides three static member functions:

.. class:: BaseField

    .. method:: split(value)

        to cup up the data into words. This function must return the words
        into the form ``(word, position)``.

    .. method:: encode(value)

        to translate the data into a storage form (a string).

    .. method:: decode(string)

        to retrieve the data from the encoded form.

For example::

    >>> from itools.xapian import make_catalog, CatalogAware
    >>> from itools.xapian import BaseField, KeywordField
    >>> from itools.xapian import register_field
    >>>
    >>> class FloatField(BaseField):
    ...     type = 'float'
    ...
    ...     @staticmethod
    ...     def split(value):
    ...         yield unicode(value), 0
    ...
    ...     @staticmethod
    ...     def decode(string):
    ...         return float(string)
    ...
    ...     @staticmethod
    ...     def encode(value):
    ...         return unicode(value)
    >>>
    >>> register_field(FloatField)
    >>>
    >>> class Document(CatalogAware):
    ...     def __init__(self, name, value):
    ...         self.name = name
    ...         self.value = value
    ...
    ...     def get_catalog_fields(self):
    ...         return [KeywordField('name', is_stored=True),
    ...                 FloatField('value', is_stored=True)]
    ...
    ...     def get_catalog_values(self):
    ...         return {'name': self.name, 'value': self.value}
    >>>
    >>> catalog = make_catalog('catalog_test')
    >>> doc1 = Document('pi', 3.1415)
    >>> doc2 = Document('e', 2.718)
    >>> catalog.index_document(doc1)
    >>> catalog.index_document(doc2)
    >>>
    >>> results = catalog.search()
    >>>
    >>> for document in results.get_documents(sort_by='value'):
    >>>     print document.name, document.value
    e 2.718
    pi 3.1415

As you can see, you must register your new type with the function
:func:`register\_field`.


Indexing, Unindexing and Transactions
=====================================

As we have seen earlier the catalog supports transactions, this means all
changes are done in memory first, and then they can be either saved or
discarded.

The operations that modify the catalog are just two:

.. method:: Catalog.index_document(document)

    Index the given document, which must be an instance of the base class
    :class:`CatalogAware`.

    If it is the later the method :meth:`get_catalog_indexes()` must be
    implemented, it will return a dictionary with the values to be indexed.

.. method:: Catalog.unindex_document(id)

    Unindex the document identified by the given external id (see section
    :ref:`xapian-external-id`).

The API to save or discard the changes is made by these two operations:

.. method:: Catalog.save_changes()

    Save the changes done so far to the catalog.

.. method:: Catalog.abort_changes()

    Discard the changes done so far to the catalog.


.. _xapian-searching:

Searching
=========

The method :meth:`search` provided by catalog objects is the entry point to
the search programming interface. Here is its prototype and definition:

.. method:: Catalog.search(query=None, \*\*kw)

    Perform a search to the catalog with the given query. Returns an instance
    of the :class:`SearchResults` class, which provides an API to retrieve the
    documents found (see below).

There are two ways to define the query, either we build it and then pass it to
the :meth:`search` method, or we use the named arguments that this method
accepts.

See now an example that shows the two ways to perform the same query. Imagine
we have a catalog of books that we index by the author and the title; and we
want to find out all the books written by somebody called Marx that talk about
money.

We can either explicitly build the query::

    >>> from itools.xapian import PhraseQuery, AndQuery
    >>>
    >>> q1 = PhraseQuery('author', 'marx')
    >>> q2 = PhraseQuery('title', 'capital')
    >>> query = AndQuery(q1, q2)
    >>> results = catalog.search(query)

Or use the named arguments::

    >>> results = catalog.search(author='marx', title='capital')

The second method is more compact, but less powerful. A query made implicitly
from named arguments will always be an "*and*" query of one or more "*phrase*"
queries.

If we want to make an "*or*" or "*range*" query, we need to build it
explicitly.


Queries
-------

Simple Queries
^^^^^^^^^^^^^^

The two most simple queries are :class:`EqQuery` and :class:`PhraseQuery`:

.. class:: EqQuery(name, value)

    Match all documents where the value of the field *name* matches or
    contains the given *value*, which will be a single word.

.. class:: PhraseQuery(name, value)

    Similar to :class:`EqQuery`, except that *value* is not a word, but a
    *phrase* (this is to say, a sequence of words).

Typically we will use phrase queries when looking for in a *text* field,
because in this context the phrase query is a generalisation of the *equal*
query::

    >>>
    # These two are the same
    >>> EqQuery('author', 'marx')
    >>> PhraseQuery('author', 'marx')
    # This is non-sense, because 'karl marx' is not a word but two
    >>> EqQuery('author', 'karl marx')

The *equal* query (:class:`EqQuery`) will be typically used for any other kind
of fields (keyword, boolean or integer). Because a phrase query is a non-sense
in this context.

To perform a :class:`EqQuery` or :class:`PhraseQuery` on a field, this one had
to be declared *indexed*.


Range Queries
^^^^^^^^^^^^^

The simple queries seen above are for exact matches. If we want to match all
values within a range we use the :class:`RangeQuery`:

.. class::  RangeQuery(name, left, right)

    Match all documents whose field *name* has a value within the given range:
    greater or equal than *left*, and lesser or equal than *right*.

    If *left* is :obj:`None`, *all* values smaller than *right* will be
    matched. If *right* is :obj:`None`, *all* values greater than *left* will
    be matched.

    At least one of the limits must be given, both *left* and *right* can not
    be :obj:`None`.

Let's see an example with dates. If we index documents by their last
modification time (*mtime*), we could search all documents that have been
modified since the last week::

    >>> from datetime import date, timedelta
    >>> from itools.xapian import RangeQuery
    >>>
    >>> today = date.today()
    >>> last_week = today - timedelta(7)
    >>>
    >>> last_week = last_week.strftime('%Y-%m-%d')
    >>> query = RangeQuery('mtime', last_week, None)

Note that since we don't have a field type for dates, we have to transform the
date values to strings (the field type used would be :class:`KeywordField`).

To perform a :class:`RangeQuery` on a field, this one had to be declared
*stored*.


Boolean Queries
^^^^^^^^^^^^^^^

We support three boolean queries:

.. class:: AndQuery(\*args)

    Match the documents that satisfy *all* the given queries. Each positional
    argument must be a query; obviously there should be two or more positional
    arguments.

.. class:: OrQuery(\*args)

    Match the documents that satisfy *any* of the given queries. Each
    positional argument must be a query; obviously there should be two or more
    positional arguments.

.. class:: NotQuery(query)

    Match all documents that are not matched by *query*.

Boolean queries can be combined to build very complex queries.


Results
-------

Now that we have built a query and performed a search, how to retrieve the
documents found? Remember that the value returned by the :meth:`search` method
is an object, instance of the :class:`SearchResults` class. This object offers
two methods:


.. class:: SearchResults

    .. method:: get_n_documents()

        Return the number of documents found.

    .. method:: get_documents(sort_by=None, reverse=False, start=0, size=0)

        Return the documents found. By default the documents are sorted by
        weight (how much relevant they are regarding the performed query).

        But the documents may also be ordered by one of the stored fields. To
        do so pass the argument *sort_by* with the name of the field to use as
        the order criteria.

        By default the results are ordered from greater to lesser (weight or
        field value). But if the argument *reverse* is :obj:`True` then they
        will be ordered in the other sense, from lesser to greater.

        It is also possible to return only a batch of the total results. To do
        so pass the arguments *start* and *size*, which indicate,
        respectively, which is the first document to return, and how many
        documents at most must be returned.

Note that to sort by a field, it must be *stored* (see section
:ref:`xapian-fields`).

Now let's see again the initial example::

    >>> results = catalog.search(body='python')
    >>> for document in results.get_documents():
    ...     print document.url
    ...
    http://www.python.org
    >>>

The thing is, the documents returned are not the original objects, but
instances of the :class:`Document` class defined by :mod:`itools.xapian`.
These *documents* offer access to the stored fields, so we can show some info
to the users without having to load the original document.

And if we want to load the original document we use the *external id* (see
section :ref:`xapian-external-id`)::

    >>> results = catalog.search(body='python')
    >>> for document in results.get_documents():
    ...     handler = get_handler(document.url)
    ...     # Do something


.. rubric:: Footnotes

.. [#xapian-xapian] http://www.xapian.org
.. [#xapian-lucene] http://lucene.apache.org/
.. [#xapian-apache] http://www.apache.org
.. [#xapian-pylucene] http://pylucene.osafoundation.org/
.. [#xapian-rq] This terminology is taken from the Lucene engine.


