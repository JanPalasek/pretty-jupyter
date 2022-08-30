Metadata
================

Metadata allow us to customize Pretty Jupyter's output report.

There are two types of metadata: notebook-level and cell-level. Notebook-level metadata specify values that are important for the entire notebook. Cell-level metadata specify values only for that particular cell.

.. note::

    Cell-level metadata have higher priority than notebook-level metadata. 

In the following section, we will look at notebook-level metadata and cell-level metadata in more details with examples.

Notebook-level Metadata
--------------------------------

Notebook-level metadata output configuration for an entire notebook.
It can be specified either in the direclty in the code, or in the notebook's metadata.

Specifying notebook-level metadata in the code is the recommended method to do it because it is well supported everywhere.
We define it by writing a **YAML header in the first raw cell of the notebook.** TODO: how to create a raw cell

.. code-block:: yaml
    :caption: Example: YAML Notebook-level metadata in the first raw cell of the notebook.

    title: "My new notebook"
    author: John Smith
    date: "{{ datetime.now().strftime('%Y-%m-%d') }}"
    output:
        general:
            input: false
        html:
            toc: false

.. note::

    Attributes `title`, `author` and `date` are processed by `Jinja templating engine <https://jinja.palletsprojects.com/>`_. This allows us to insert more complex expressions than a simple text, such as generate current date.

    For security reasons, the number of available available variable names in Jinja is restricted to `datetime` and notebook-level metadata available under `resources`.


Alternatively, we can describe notebook-level metadata directly in the notebook metadata. We open the notebook's metadata and
create a new attribute `pj_metadata`. We specify the the metadata values in json format.

.. code-block:: json
    :caption: Example: Notebook-level metadata in notebook's metadata.

    {
        "pj_metadata": {
            "title": "My new notebook",
            "author": "John Smith",
            "date": "{{ datetime.now().strftime('%Y-%m-%d') }}",
            "output": {
                "general": {
                    "input": false
                },
                "html": {
                    "toc": false
                }
            }
        }
    }

.. note::

    Both Jupyter and JupyterLab have a UI support for specifying notebook-level metadata.
    In other environments (such as VSCode or Pycharm), we need to *open the notebook as a text file* and find "metadata" section of the notebook.
    It is usually located at the end of the notebook's json code.


Cell-level Metadata
--------------------------

Cell-level metadata allow us to alter exporting behavior for the particular cell of the notebook.

Similarly to notebook-level metadata, there are two ways to specify it: either directly in the code, or using cell metadata.

In the code, we need to specify it in the first line of code.

.. code-block:: python
    :caption: Example: Python code cell with cell-level metadata.

    # -.-|m { input: true, output_error: false, input_fold: show }
    # now we can write normla code cell
    a = 10
    a *= 3

In the Jinja Markdown cell, we specify it in the first line of code after specifying Jinja Markdown cell-level magic (the `%%jmd` tag).

.. code-block:: markdown
    :caption: Example: Jinja Markdown cell with cell-level metadata.

    %%jmd
    [//]: # (-.-|m { input: true, output_error: false, input_fold: show })

    Here we can write normal Jinja markdown as usual.

To specify it in the notebook's metadata, we need to find the cell's metadata and add new `pj_metadata`, as can be seen in the next example.

.. code-block:: json
    :caption: Example: Cell-level metadata in notebook's metadata.

    {
        "pj_metadata": {
            "input": true,
            "output_error": false,
            "input_fold": "show"
        }
    }

.. note::

    Both Jupyter and JupyterLab have a UI support for specifying cell-level metadata.
    In other environments (such as VSCode or Pycharm), we need to *open the notebook as a text file*, find the section
    of the particular cell and specify the metadata there. Note that the cell outputs also have metadata (it is mess).
    Without the support from UI, it is highly recommended to specify it in the code.



Metadata Options
-------------------

.. list-table:: Notebook-level metadata options
    :widths: 25 25 50
    :header-rows: 1

    *
        - Name
        - Values
        - Description
    *
        - title
        - string
        - Title of the output report.
    *
        - author
        - string
        - Author of the notebook.
    *
        - date
        - string
        - | Date of the report.
          | E.g. when it was generated.
    *
        - output.general.input
        - boolean, default: true
        - | If true, then the input of code cells
          | will be included in the report.
    *
        - output.general.input_jinja
        - boolean, default: false
        - | If true, then input of Jinja cells
          | will be included in the report.
    *
        - output.general.output
        - boolean, default: true
        - | If true, then output of code cells
          | will be included in the report.
    *
        - output.general.output_error
        - boolean, default: false
        - | If true, then error outputs
          | will be included in the report.
    *
        - output.general.output_stdout
        - boolean, default: true
        - | If true, then stdout outputs
          | will be included in the report.
          | An example of stdout output is
          | the output of `print` function.
    *
        - output.html.toc
        - boolean, default: true
        - | If true, then Table of Contents
          | is automatically generated.
    *
        - output.html.toc_depth
        - int, default: 3
        - | Number of sections that are
          | taken into account by TOC.
    *
        - output.html.toc_collapsed
        - boolean, default: true
        - | If true, then the generated TOC
          | is expanded and doesn't reveal or
          | hide sections on scroll.
    *
        - output.html.toc_smooth_scroll
        - boolean, default: true
        - | If true, then scrolling is smooth
          | on clicking on TOC section.
    *
        - output.html.number_sections
        - boolean, default: false
        - | If true, then automatic section
          | numbering is added to section
          | names.
    *
        - output.html.code_folding
        - | choice [hide, show, disable],
          | default: hide
        - | hide: Code is hidden at the start.
          | show: Code is shown at the start.
          | disable: Code folding is disabled.
    *
        - output.html.tabset
        - boolean, default: true
        - | If **false**, then tabsets
          | aren't generated.
    *
        - output.html.theme
        - choice, default: paper
        - | Specifies visual (bootstrap) theme
          | of the output html page.
    *
        - output.pdf.toc
        - boolean, default: true
        - | If true, then TOC
          | is generated for output
          | pdf report.
    *
        - output.pdf.toc_depth
        - int, default: 3
        - | Number of sections that are
          | taken into account by TOC.
    *
        - output.pdf.language
        - string, default: english
        - | Specifies language for
          | latex babel package.


.. list-table:: Cell-level metadata options
    :widths: 25 25 50
    :header-rows: 1

    *
        - Name
        - Values
        - Description
    *
        - input
        - | boolean
        - | If true, then the input
          | is in the output report.
    *
        - input_fold
        - choice [hide, show]
        - | hide: If code-folding
          | is enabled, the input
          | is hidden at the beginning.
          | show: The input is shown
          | at the beginning.
    *
        - output
        - boolean
        - | If false, then outputs
          | are not included.
    *
        - output_error
        - boolean
        - | If true, then error
          | outputs are not included.
    *
        - output_stdout
        - boolean
        - | If true, then stdout
          | outputs are not include.
          | Example of stdout output
          | is output of `print` function.

.. note::

    Defaults of cell-level metadata come from corresponding notebook-level metadata.

Priority
-----------

The priority can be explained by the following statement:

    **More specific settings have a higher priority than less specific settings.**

More specifically:

- Cell-level metadata have higher priority than notebook-level metadata.
- More specific notebook-level or cell-level metadata override the less specific ones.

We will demonstrate this on a couple of examples:

- If cell has `input: true` and it is a Jinja Markdown cell, than this overrides any other settings. It beats notebook-level `input: false` and `input_jinja: false`.
- If cell has `output_error: true`, then for an error output this has a higher priority than cell-level `output: false` or notebook-level `output_error: false` and `output: false`.

.. note::

    A one exception from this rule is code folding. If it is disabled on the
    notebook-level, then the cell-level settings are ignored.


Examples
----------

Check out our `example repository <https://github.com/JanPalasek/pretty-jupyter-examples>`_ for this and more examples. Specifically:

- **metadata**: Demonstrates basic examples that show how to use metadata in your project.
