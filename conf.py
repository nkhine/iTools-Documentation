# -*- coding: utf-8 -*-
#
# HForge documentation build configuration file, created by
# sphinx-quickstart on Mon Feb 16 11:48:38 2009.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# We need an installed itools for the itools-api directory
try:
    import itools
except ImportError:
    print "\nError: You must first install itools on your python"
    exit(1)

# If your extensions are in another directory, add it here. If the directory
# is relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
#sys.path.append(os.path.abspath('.'))

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'HForge'
copyright = u'2009, Juan David Ibáñez Palomar'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.50'
# The full version, including alpha/beta/rc tags.
release = '0.50'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
unused_docs = ['ikaaro/developers']

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['.build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# Options for HTML output
# -----------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
html_style = 'hforge.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "HForge's documentation center"

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "HForge's documentation"

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['.static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {'download': 'download.html'}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'HForgedoc'


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
latex_paper_size = 'a4'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).

jdavid = ur'Juan David Ibáñez Palomar'
latex_documents = [
  ('itools/index', 'itools-tutorial.tex', ur"Itools' tutorial", jdavid,
   'manual'),
  ('ikaaro/users', 'user-guide.tex', ur"User Guide", jdavid, 'howto'),
  ('ikaaro/admins', 'administrator-guide.tex', ur"Administrators Guide",
   jdavid, 'howto'),
  ('i18n/index', 'i18n.tex', ur"Internationalization", jdavid, 'howto'),
  ('git/index', 'git.tex', ur"Introduction to Git", jdavid, 'howto'),
  ('style/index', 'style.tex', ur"Coding Style", jdavid, 'howto'),
  ('packaging/index', 'packaging.tex', ur"The itools packaging system",
   jdavid, 'howto'),
  ('windows/index', 'windows.tex', ur"Build Itools under Windows", jdavid,
   'howto'),
# NotImplementedError: Column or row spanning cells are not implemented.
#  ('localizer/index', 'localizer.tex', ur"Localizer", jdavid,
#   'howto')
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True

# Options for the autogenerated documentation
autodoc_member_order = 'groupwise'

# Populate the itools-api/modules path
def setup(app):
    # Imports
    from os import mkdir, listdir
    from os.path import join, exists, isdir

    # Template to make the files in itools-api/modules
    template_module = """:mod:`itools.{module}`
##############################################
.. automodule:: itools.{module}
   :synopsis: {synopsis}
   :show-inheritance:
   :members:
   :undoc-members:
   :noindex:
"""

    # Make the itools-api/modules directory
    mods_path = join('itools-api', 'modules')
    if not exists(mods_path):
        mkdir(mods_path)

    # Make the itools-api/modules/*.rst files
    installed_mods = listdir(mods_path)
    itools_path = itools.__path__[0]
    for module in listdir(itools_path):
        if ( isdir(join(itools_path, module)) and
             module not in ('doc', 'locale') ):

            # Already save ?
            if (module + '.rst') in installed_mods:
                continue

            # Try to catch its __doc__
            doc = None
            try:
                __import__("itools.%s" % module)
                doc = itools.__dict__[module].__doc__
            except (ImportError, KeyError):
                pass

            # Make the Synopsis
            if doc is not None:
                synopsis = doc.split('\n\n')[0]
            else:
                synopsis = "Itools %s module" % module

            # And the save the file
            print '[itools-api] make the modules/%s.rst file' % module
            rst_file = open('itools-api/modules/%s.rst' % module, "w")
            rst_file.write(template_module.format(module=module,
                                                  synopsis=synopsis))
            rst_file.close()
