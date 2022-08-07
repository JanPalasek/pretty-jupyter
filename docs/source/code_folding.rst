Code Folding
================

Code Folding is a functionality that allows us to show or hide input of the code cells. This allows us to reduce the visual clutter on the output page.

.. _code-folding-figure:
.. figure:: _static/code-folding.png
    :class: no-scaled-link
    :scale: 50 %
    :alt: Code folding.

    Figure: Code Folding

By pressing Hide (Show resp.) the code disappears (appears resp.). We can also hide or show all codes thanks to the option in the right upper corner.

Code Folding can be set up by specifying the following attributes in the notebook's metadata:

* ``"code_folding": "show"``: Code Folding is enabled and all cells are shown at the beginning.
* ``"code_folding": "hide"``: Code Folding is enabled and all cells are hidden at the beginning. **This is a default behavior.**
* ``"code_folding": null``: Code Folding is disabled. The input cells are all visible in the report (unless configured otherwise) and cannot be hidden.

