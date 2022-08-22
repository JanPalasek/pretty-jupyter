Metadata
================

Often we want to e.g. change the output's title. This is done using metadata. There are two types of metadata: notebook-level and cell-level. Notebook-level metadata specify values that are important for the entire notebook. Cell-level metadata specify values only for that particular cell. **Cell-level metadata have higher priority than notebook-level metadata.** 

In the following section, we will look at notebook-level metadata and cell-level metadata in more details with examples.

Notebook-level metadata
--------------------------------

Notebook-level metadata specify values for an entire notebook. It can be specified either in the first cell of the notebook that is of a raw type, or in the notebook's metadata.


Specifying notebook-level metadata in the first raw cell is a recommended method because it is well supported on every platform. We do it by writing a "YAML header", which describes the metadata values in a easily readable and writable format.

.. note::

    Attributes `title`, `author` and `date` are processed by Jinja (TODO) templating engine. This allows us to insert more complex expressions than a simple text, such as generate current date.

    For security reasons, the number of available available variable names in Jinja is restricted to `datetime` and notebook-level metadata available under `resources`.

.. code-block:: yaml
    :caption: YAML Notebook-level metadata.

    title: "My new notebook"
    author: John Smith
    date: "{{ datetime.now().strftime('%Y-%m-%d') }}"
    output:
        general:
            input: false
        html:
            toc: false

Alternatively, we can describe notebook-level metadata directly in the notebook metadata. Both Jupyter and JupyterLab have a UI support for this task (TODO: where).

In other environments (such as VSCode or Pycharm), we need to *open the notebook as a text file* and "metadata" section for the notebook. It is usually at the bottom of the notebook. There we create a new attribute `pj_metadata` and specify the same values as we would in the structure header.

.. code-block:: json
    :caption: Notebook-level metadata in notebook's metadata.

    {
        "metadata": {
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
    }

TODO: where is list of all supported expressions

Cell-level metadata
--------------------------



