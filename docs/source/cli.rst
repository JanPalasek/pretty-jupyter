Command-line Interface
==========================

Pretty Jupyter has a rich command-line interface. This is thanks to `nbconvert <https://github.com/jupyter/nbconvert>`_, which it internally uses.

The basic use of Pretty Jupyter is the following:

.. code-block:: bash
    :caption: Basic command

    jupyter nbconvert --to html --template pj /path/to/ipynb/file

This exports the notebook file in the html located in the same directory, but with a different extension.

Notable switches
---------------------

The most notable switches are the following:

* ``--no-input``: Doesn't generate the input (at all).
* ``--embed-images``: All image links are embedded directly to the html page. This is good for a standalone report.

Furthermore, we can override default behavior with the following commands:

* ``--RemoveOutputPreprocessor.stream_stderr=0`` together with ``--RemoveOutputPreprocessor.output_error=0``: By default, all error stream outputs are removed (standard output errors are left in). This makes for a nicer reports. However, these settings cause that the error outputs will be left in.
* ``--RemoveInputPreprocessor.jinja=1``: Jinja Markdown inputs are by default removed from the html. This will also export them. This is sometimes useful for demonstration purposes.

Check out `nbconvert's documentation <https://nbconvert.readthedocs.io/en/latest/config_options.html>`_ for more switches. Ignore those that are irrelevant for HTML.