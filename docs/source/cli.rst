Command-line Interface
==========================

Pretty Jupyter has a rich command-line interface. This is thanks to `nbconvert <https://github.com/jupyter/nbconvert>`_, which it internally uses.

The basic use of Pretty Jupyter is the following:

.. code-block:: bash
    :caption: Basic command

    jupyter nbconvert --to html --template pj /path/to/ipynb/file

This exports the notebook file into the html located in the same directory.

Switches
---------------------

We can override notebook-level metadata (see :ref:`Metadata:Notebook-level Metadata`) with specifying `--HtmlNbMetadataPreprocessor.pj_metadata`. We specify 
our desired notebook-level metadata configuration in YAML, for example:

.. code-block:: bash
    :caption: Notebook-level metadata override

    jupyter nbconvert --to html --template pj /path/to/ipynb/file --HtmlNbMetadataPreprocessor.pj_metadata "{ output: { html: { toc: false } } }"

This will override the default value and prevent Table of Contents from being generated.

We can also use multi-line yaml.

.. code-block:: bash
    :caption: Notebook-level metadata override

    jupyter nbconvert --to html --template pj /path/to/ipynb/file --HtmlNbMetadataPreprocessor.pj_metadata "
    output:
        html:
            toc: false
    "

Other notable switches:

* ``--embed-images``: All image links are embedded directly to the html page. This is good for a standalone report.
* ``--no-input``: Doesn't generate the input (at all). Ignores all metadata configuration.

Check out `nbconvert's documentation <https://nbconvert.readthedocs.io/en/latest/config_options.html>`_ for more switches. Ignore those that are irrelevant for HTML.

Templates
------------