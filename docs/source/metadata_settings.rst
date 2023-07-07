Metadata Options
====================

This page is a definite list of all notebook-level and cell-level metadata options with their description.

Notebook-Level
-------------------------

.. list-table::
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
        - output.html.toc_extend_page
        - boolean, default: true
        - | If true, then page is slightly
          | extended to make TOC work
          | better.
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
        - output.html.code_tools
        - boolean, default: false
        - | If true, then a button
          | is added which can show 
          | or hide code all at once.
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

Cell-Level
----------------------

.. list-table::
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