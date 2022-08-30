Styling
===============

Basics
--------

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


Targeting Elements
-------------------------

Pretty Jupyter allows us to add classes and IDs to elements. Usually we do this with markdown elements because basic Markdown doesn't support adding custom classes to them.

The following block demonstrates this as an example. The line below the table adds two classes and specifies the id to the table. Therefore, the output table will have classes custom-class-1 and custom-class-2 and it will have id my-table-id.

.. code-block:: markdown
    :caption: Example: Targeting table.

    | col1 | col2 |
    |------|------|
    | val1 | val2 |

    [//]: # (-.- .custom-class1 custom-class2 #my-table-id)

We call the line under the table a **token specifier**.

This functionality is not limited for tables. It can be applied to **any** markdown or html element. Even to a paragraph:

.. code-block:: markdown
    :caption: Example: Targeting paragraph.

    This paragraph will be a warning alert.

    [//]: # (-.- .alert .alert-warning)

.. note::

    Markdown automatically creates paragraph elements from the text separated by newlines.

.. important::

    **Placing token specifier under the header will modify the section, not the header.** This behavior is used to specify tabsets or headers that are ignored by Table of Contents.


There are a lot of already existing classes from Boostrap 3 or Pretty Jupyter that can be used to make the report prettier. We list the main ones in the following subsections.


Header (Section)
~~~~~~~~~~~~~~~~~~

- `tabset`: Transforms the section from linear structure into a tabset.
- `tabset-pills`: Changes the visual design of the tabs.
- `tabset-fade`: Adds fluent animation when switching the tabs.
- `toc-ignore`: Is ignored by Table of Contents.
- `unlisted`: The section is not listed in the Table of Contents.
- `unnumbered`: If section numbering is turned on, this section is not numbered.

Table
~~~~~~~~~~~~~~~~~~
- `pj-table-ignore`: All tables have basic table styling added by Pretty Jupyter. This class makes it so default styling is not applied to them.
- `pj-table-fit`: The table is shrunk around its content.
- `table`: Basic bootstrap styling.

Paragraph
~~~~~~~~~~~~~~~~~~
- `bg-info`: Changes background of the paragraph to "info" color from bootstrap. Other options: `bg-warning`, `bg-danger`.
- `alert`: Makes paragraph into an alert. Should be used together with `alert-info`, `alert-warning`,...


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