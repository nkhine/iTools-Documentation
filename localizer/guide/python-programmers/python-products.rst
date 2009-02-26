Python products
===============

The Localizer product also provides facilities to internationalize and
localize python products. These facilities are built around the GNU gettext
utilities, the standard in the free software community.


Internationalize
----------------


* DTML and ZPT

    The LocalDTMLFile and LocalPageTemplateFile classes must be used instead
    of the DTMLfile and PageTemplateFile classes::

        from Products.Localizer import LocalDTMLFile, LocalPageTemplateFile

        ....

        manage_addForm = LocalDTMLFile('addForm', globals())

    Then the messages will be translated using the gettext method:

    .. code-block:: xml

        <dtml-var "gettext('Hello world!')">
        <span tal:replace="python:gettext('Hello world!')">
          Hello world!
        </span>


* Python code

    Import the needed stuff::

        from Products.Localizer import Gettext

        _ = Gettext.translation(globals())
        N_ = Gettext.dummy

    The underscode (\_) is used to translate messages. The N\_ function is
    used for defered translations, it markups the message for translation but
    don't translates it.
    ::

        def x(self, ...):
            return _('Hello world!')


Localize
--------

The messages and their translations are stored in ".po" and ".mo" files, in
the locale directory within the product.

To help with the localization task Localizer includes the script zgettext.py.
Use it from your product directory, for example:

.. code-block:: sh

    ../Localizer/zgettext.py *.dtml -l es fr

will create the locale directory and the locale.pot, es.po and fr.po files
inside. Then the human translators will translate the messages in the ".po"
files. Finally, type:

.. code-block:: sh

    ../Localizer/zgettext.py -m

to compile the ".po" files and generate the ".mo" files that will be used at
run time to get the translations.


Unicode
-------

Besides the gettext method the ugettext one is also available. Both methods
have the same interface, the difference is that ugettext returns unicode
strings.


