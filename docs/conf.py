# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
import os, sys
import sphinx_rtd_theme
from recommonmark.parser import CommonMarkParser

sys.path.insert(0, os.path.abspath("../Aeros"))
sys.path.insert(0, os.path.abspath("../Python/"))

project = 'Aeros'
copyright = '2020, TheClockTwister'
author = 'TheClockTwister'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'recommonmark',  # Markdown support (needs package "recommonmark")
    'sphinx.ext.napoleon',  # needs to be before "sphinx_autodoc_typehints"-m
    'sphinx_rtd_theme',
    'autoapi.extension',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_annotation'
]

source_parsers = {".md": CommonMarkParser}

autoapi_type = 'python'
autoapi_dirs = [os.path.abspath("../Aeros")]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_css_files = ['custom.css']
html_logo = "_static/logo.png"
html_theme_options = {
    'logo_only': True,
    'display_version': False,
    "collapse_navigation": False
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}
