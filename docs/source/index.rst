=================
Pretty Jupyter
=================

Pretty Jupyter is an easy-to-use package that allows to create beautiful & dynamic html reports. Its main features are:

- **Visually appealing styles**.
- **Table of Contents** can be automatically generated.
- Using **Python variables in Markdown**.
- **Tabsets** for hiding section content behind clickable tabs.
- **Code Folding**: Show/Hide code to filter out unnecessary content.
- **Themes**: Selection from a wide variaty of available themes.
- **Wide range of configuration options** with sensible defaults. 
- **Unobtrusive syntax** that works well in notebook environments.

All these features are integrated directly in the output page, therefore there is no need to have an interpreter running in the backend. This makes the html easily sendable or uploadable to a static website.

**Most of the features require a little to no work to get working** and greatly improve the quality of the output report, or even the developer's comfort when creating the report. For example, tabs make some visualizations much more comfortable.

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
   :caption: Basics

   quickstart
   page_header
   jinja_markdown
   tabset
   toc
   code_folding
   cli
   pdf

.. toctree::
   :maxdepth: 2
   :caption: Customizing Output

   metadata
   styling
   custom_template

.. toctree::
   :maxdepth: 2
   :caption: Configuration Options

   metadata_settings
   styling_settings
   cli_settings

.. toctree::
   :maxdepth: 2
   :caption: About

   changelog

Credits
==========

* **RMarkdown**: RMarkdown served as a great inspiration when making this package. Most of the functionality is inspired by it.
* **nbconvert**: Pretty Jupyter uses nbconvert underhood. Its great extendability allowed this project to be created.
* **ReadTheDocs**: This awesome project allows you to host your documentation for free, improving the repo quality worldwide.
