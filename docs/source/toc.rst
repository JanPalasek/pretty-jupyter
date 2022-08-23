Table of Contents
======================

Pretty Jupyter automatically generates Table of Contents for the page. The table of contents looks as below:

.. _toc-figure:
.. figure:: _static/toc.png
    :scale: 50 %
    :alt: Table of Contents output.

    Figure: Table of Contents

.. note::
    Each header from the notebook is automatically added to the Table of Contents.

    We can prevent a header from being added to the Table of Contents by adding class ``toc-ignore``. We cannot do this with Markdown syntax,
    however we can do this in HTML.
    
    For example: ``<h2 class='toc-ignore'>Header that is not in TOC</h2>``

To turn off Table of Contents functionality completely, we need to add the following property to the notebook metadata: ``"toc": false``.

Examples
--------------------

Check out more examples in our `example repository <https://github.com/JanPalasek/pretty-jupyter-examples>`_. Specifically, the TOC are demonstrated in the following example:

* **main-features-demo**: Practical example for a tabset feature.