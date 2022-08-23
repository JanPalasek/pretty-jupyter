Styling
===============

We can apply custom styles to modify the page to our needs.

The simplest way to do this is by using ``<style>`` tags and use standard CSS to do the job. We can use those tags e.g. in Markdown or Jinja Markdown cells.

For example:

.. code-block:: python

    %load_ext pretty_jupyter

.. code-block:: markdown
    
    %%jinja markdown

    <style>
        h2 {
            background-color: red;
            color: white;
        }
    </style>

    ## Level 2 Header

    ### Level 3 Header

    <style>
        h3 {
            background-color: blue;
            color: white;
        }
    </style>

    ## Another Level 2 Header

.. _styling-example-figure:
.. figure:: _static/styling-example.png
    :class: no-scaled-link
    :scale: 50 %
    :alt: Styling example output.

    Figure: Styling example output


Themes
-------------

We can customize the general theme of the page. To do this, we specify ``theme`` attribute in the notebook's metadata.

Currently, there are three themes supported, all thanks to  `bootswatch project <https://bootswatch.com/3/>`_:

* **paper**: Default. Light.
* **journal**: Light. Different color-set.
* **slate**: Dark.

For example, to use journal theme, write this in your notebooks metadata:

.. code-block:: yaml

    output:
        html:
            theme: journal

This will include embed your theme directly in the output.

You can also use any bootstrap 3 theme (for example the ones from `bootswatch <https://bootswatch.com/3/>`_). For example:

.. code-block:: yaml

    output:
        html:
            theme: https://bootswatch.com/3/sandstone/bootstrap.min.css

Examples
--------------------

Check out more examples in our `example repository <https://github.com/JanPalasek/pretty-jupyter-examples>`_.
Themes are specifically demonstrated in **themes** example, where we apply dark theme on a simple notebook.