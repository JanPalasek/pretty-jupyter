Quick Start
=========================

Installation
-----------------

Nbconvert is packaged for both pip and conda, so you can install it with the following command.

.. code-block::

    pip install pretty-jupyter


Usage
-----------

After installation, we can run Pretty Jupyter using the following command:

.. code-block::

    jupyter nbconvert --to html --template pj /path/to/ipynb/file

.. seealso::
    Pretty Jupyter uses nbconvert's underhood including its command line interface. Check out `its documentation <https://nbconvert.readthedocs.io/>`_.

It generates the output html file to the same directory as was the input file. It has a lot of the functionality built-in in the defaults, such as:

* **Visually appealing styles**
* **Automatic Table of Contents generation**.
* **Code Folding**: Show/Hide buttons.

Other functions need the notebook to be customized a little bit. Example of such functions:

* **Jinja Markdown**: An ability to write Markdown with using Python variables inside. Allows for dynamic reports.
* **Tabset**: Shows specified sections as clickable panels instead of a scrollable content.