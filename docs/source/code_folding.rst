Code Folding
================

Code Folding is a functionality that allows us to show or hide input of the code cells. This allows us to reduce the visual clutter on the output page.

TODO: example

By pressing Hide (Show resp.) the code disappears (appears resp.). We can also hide or show all codes thanks to the option in the right upper corner.

Code Folding is by default turned on for all code cells and the input of the cells is by default hidden. We can modify this behavior in the notebook metadata:

* ``"code_folding": "show"``: Code Folding is enabled and all cells are shown at the beginning.
* ``"code_folding": "hide"``: Code Folding is enabled and all cells are hidden at the beginning. **This behavior is default.**
* ``"code_folding": null``: Code Folding is disabled. The input cells are all visible in the report (unless configured otherwise) and cannot be hidden.
