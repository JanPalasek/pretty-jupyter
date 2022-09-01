CLI Options
===================================

This page provides a list of important settings that can be used from command-line to alter the appearance or behavior of the output.

.. note::
    Since Pretty Jupyter is built upon nbconvert, you can also use their switches. Checkou out `its documentation <https://github.com/jupyter/nbconvert>`_ for more available settings.

Main Switches
---------------------------

* ``--to``: Specifies the output format. Currently supported options are ``html`` and ``pdf``. Pdf is experimental.
* ``--template``: Specifies template that will be used to generate the output. For ``--to html`` use ``--template pj``. If you like the old design more, use ``--template pj-legacy``. For ``--to pdf`` use ``--template pj-pdf`` (experimental).

If you want to use a custom template, you need to also use ``--TemplateExporter.extra_template_basedirs=path/to/dir/with/template``. The value of ``--template`` should reflect the template directory name. Check out :doc:`custom_template` page for more information about how to create a custom template.


Other Switches
-------------------------

* ``--embed-images``: All image links are embedded directly to the html page. This is good for a standalone report.
* ``--no-input``: Doesn't generate the input (at all). Ignores all metadata configuration.
* ``--execute``: Executes all cells of the notebook before the export.
* ``--allow-errors``: If an error is encountered during the execution, the execution continues with the rest of the cells instead of stopping.

Notebook-Level Metadata
------------------------------------

.. code-block:: bash
    :caption: One-line yaml metadata

    jupyter nbconvert --to html --template pj /path/to/ipynb/file --HtmlNbMetadataPreprocessor.pj_metadata "{ output: { html: { toc: false } } }"


We can also use multi-line yaml for better visual clarity:

.. code-block:: bash
    :caption: Multi-line yaml metadata

    jupyter nbconvert --to html --template pj /path/to/ipynb/file --HtmlNbMetadataPreprocessor.pj_metadata "
    output:
        html:
            toc: false
    "

Check out :ref:`metadata_settings:Notebook-Level` section to see all the definite list of options that can be overidden.

.. note::
    When using ``--tepmlate pj-pdf``, instead of ``--HtmlNbMetadataPreprocessor``, we need to use ``--NbMetadataPreprocessor``.