Tabset
================

Pretty Jupyter allows us to generate tabset from the specified sections.
It allows readers to view the content of different sections by clicking the tab header instead of scrolling back and forth on the page.

We can generate a tabset by adding the following line under a header that we want to be a tabset root: ``[//]: <> (-.- tabset)``. We call this line a tabset specifier.

.. _simple-tabset-code:
.. code-block::
    :caption: Code: Tabset input

    ## Tabset
    [//]: <> (-.- tabset)

    ### First Tab
    Content of this first section will be generated into the first tab content.

    ### Second Tab
    Same goes for the second section.

The output of the tabset is demonstrated in the figure below.

.. _simple-tabset-figure:
.. figure:: _static/tabset.png
    :class: no-scaled-link
    :scale: 50 %
    :alt: Tabset output.

    Figure: Tabset output


.. note::
    The content of tabsets don't have to be all in one cell. For example the "First Tab" cell in the :ref:`simple-tabset-code` could be placed in a different cell than "Second Tab" and "Tabset".
    There can be any number of cells between them.

.. note::
    Tabset is also supported in Jinja Markdown cells.


We can also provide an alternative look to the tabset. We can specify ``[//]: <> (-.- tabset tabset-pills)``, which causes Pretty Jupyter to output tabset below.

.. _tabset-pils-figure:
.. figure:: _static/tabset-pills.png
    :class: no-scaled-link
    :scale: 50 %
    :alt: Tabset-pills output.

    Figure: Tabset-pills output


**In general, the tabs are generated from the child sections of a section that has a tabset specifier under it**. We call such a section a tabset root.
The tabset ends if we specify a section that has same or higher level as the tabset root.

We can use this behaviour to our advantage and use an empty header element just to end the tab section and write a text further below.

.. _tabset-trick:
.. code-block::
    :caption: Code: Tabset trick

    ## Tabset
    [//]: <> (-.- tabset)

    ### First Tab
    Content of this first section will be generated into the first tab content.

    ### Second Tab
    Same goes for the second section.

    <h2 class="toc-ignore"></h2>

    Text that will not appear in the tabs but below them instead.


Check out more examples in our `example repository <https://github.com/JanPalasek/pretty-jupyter-examples>`_. Specifically, the tabsets are demonstrated in the following examples:

* demo: A simple demo of app functionality. Contains a few tabsets of "pills" type.
* main-features-demo: Practical example for a tabset feature.
* dynamic-tabsets: An advanced application of tabsets. The tabsets are dynamically generated using Jinja Markdown.


