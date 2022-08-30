=================
Pretty Jupyter
=================

Pretty Jupyter is an easy-to-use package that allows to create beautiful & dynamic html reports. Its main features are:

   - Visually appealing styles.
   - Automatic Table of Contents generation.
   - Using Python variables in Markdown (aka Jinja Markdown).
   - Tabsets: tabs that hold section content inside them.
   - Code Folding: Show/Hide code to filter out unnecessary content.

All these features are integrated directly in the output page, therefore there is no need to have an interpreter running in the backend. This makes the html easily sendable or uploadable to a static website.

Syntax of Pretty Jupyter is unobtrusive and designed to work well in notebook environments like JupyterLab etc. Most of the features require a little to no work to get working and greatly improve the quality of the output report, or even the developer's comfort when creating the report.

To use Pretty Jupyter, all we need are two commands: install and export.

.. code-block:: bash

   # install
   pip install pretty-jupyter
   # export
   jupyter nbconvert --to html --template pj /path/to/ipynb/file

Contents
============

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   getting_started
   jinja_markdown
   tabset
   toc
   code_folding
   styling
   custom_template
   metadata
   cli
   pdf

.. toctree::
   :maxdepth: 2
   :caption: About

   changelog

Credits
==========

* **nbconvert**: Pretty Jupyter uses nbconvert underhood. Its great extendability allowed this project to be created.
* **RMarkdown**: RMarkdown served as a great inspiration when making this package.
* **ReadTheDocs**: This awesome project that allows you to host your documentation for free, improving the repo quality worldwide.
