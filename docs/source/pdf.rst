PDF
======

Although the main goal of this project is to have a beautiful HTML reports, there is also support for PDF reports.

There are two methods of generating PDF report: HTML with browser export and PDF via Latex.

PDF from HTML
-----------------

The first way of generating PDF is the following:

1. Generate HTML report.
2. Open it in your browser.
3. Export it to PDF from the browser (Ctrl + P).

To improve the output PDF styles, we should disable the dynamic elements that have no meaning in the result PDF.
The next code block demonstrates, which settings we should focus on.

.. code-block:: yaml

    output:
        html:
            toc: false
            tabset: false
            code_folding: disable

.. important::
    This is the recommended way of generating markdown.


PDF via Latex
---------------

We can also export PDF via Latex. This can be done by the following command:

.. code-block:: bash

    jupyter nbconvert --to html --template pj-pdf /path/to/ipynb/file

To use this, **we need to have pandoc installed.** To install pandoc on Linux, you can generally use package manager:

.. code-block:: bash

    sudo apt-get install pandoc

On other platforms, you can get pandoc from `their website <https://pandoc.org/installing.html>`_.

.. note::

    To provide custom overrides for metadata, instead of ``--HtmlNbMetadataPreprocessor``, we need to use ``--NbMetadataPreprocessor``.

The export can be customized by overriding values in pdf section of the metadata configuration. Check out :ref:`Metadata:Metadata Options` for more information.