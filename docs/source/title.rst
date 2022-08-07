Page Title
================

Page title is by default set to the name of the file. To override this behavior, we specify ``"title"`` attribute in the notebook's metadata. For example:

.. code-block:: json

    "metadata": {
        "title": "My New Title",
    }

.. note::
    Some environments, such as JupyterLab and Jupyter, support specifying notebook metadata in their UI.
    
    In others, we need to open the notebook file as a text, locate "metadata" attribute in its json and write the title there directly.