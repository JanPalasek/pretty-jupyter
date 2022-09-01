Page Header
==============

In this page, we describe, how to set up a page header.

The most easy way to set up a page header is to create a first cell of a **raw type**. In this cell, we specify the header in yaml.

The next code block shows an example of such a header.

.. code-block:: yaml

    title: Page Title
    author: Page Author
    date: "{{ datetime.now().strftime('%Y-%m-%d') }}"

.. note::
    A header similar to this is automatically generated when starting a new report with a command ``pretty-jupyter quickstart path/to/output/ipynb``.

There are many more properties that can be set in the header. Check out :doc:`metadata` page for more detailed information about page header's options and how it works.