# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# pylint: disable=invalid-name
# pylint: disable=redefined-builtin
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.append(
    os.path.abspath("../../")
)  # This is so sphinx knows where to find your module
html_logo = "../../pictures/groucho_small.png"  # adds logo to documents pages.

project = "Record Synthesizer"
author = "Kevin J. Delaney"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx_markdown_builder",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
