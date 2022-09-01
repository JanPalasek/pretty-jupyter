Styling Options
==================

This page contains list of styling settings.

Header (Section)
-------------------------------

This section specifies classes that can be used to modify the header (its section respectively). Check out :ref:`styling:Targeting Elements` for more information about this functionality.

.. note::
    
    This is not a definite list. There are many other classes and you can also add your own ones.

- ``.tabset``: Transforms the section from linear structure into a tabset.
- ``.tabset-pills``: Changes the visual design of the tabs.
- ``.tabset-fade``: Adds transition animation when switching the tabs.
- ``.unnumbered``: If section numbering is turned on, this section is not numbered.
- ``.unlisted``: If used together with ``.unnumbered``, then hte section is omitted from the table of contents.

Others
-----------

This section specifies classes that can be used to modify other elements. Check out :ref:`styling:Targeting Elements` for more information about this functionality.

.. note::
    
    This is not a definite list. There are many other classes to style the elements. You can also add your own ones.

- ``.pj-table-fit``: The table is shrunk around its content.
- ``.pj-table-ignore``: All tables have basic table styling added by Pretty Jupyter. This class makes it so default styling is not applied to them.
- ``.bg-info``: Changes background of the element to "info" color from the theme. Other options: ``.bg-warning``, ``.bg-danger``.
- ``.alert``: Makes element into an alert. Should be used together with ``.alert-info``, ``.alert-warning``,...

Themes
-----------

Currently, all `bootswatch themes <https://bootswatch.com/3/>`_ are supported with the default bootstrap theme. We can use them by e.g. specifying theme in :ref:`metadata_settings:Notebook-Level` metadata.

The entire list of supported themes is: ``bootstrap``, ``cerulean``, ``cosmo``, ``cyborg``, ``darkly``, ``flatly``, ``journal``, ``lumen``, ``paper`` (default), ``readable``, ``sandstone``, ``simplex``, ``slate``, ``spacelab``, ``superhero``, ``united``, ``yeti``.