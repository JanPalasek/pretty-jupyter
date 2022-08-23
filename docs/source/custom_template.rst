Custom Template
==========================

In some instances, we need to customize the page even more than the other tools allow us. The typical scenarios might be these:

* We want to apply the same styles or changes to all our reports.
* We want to change to change behavior of the default template, which does not suit us.

Pretty Jupyter handles these situations by allowing us to extend the basic template.

How to Extend
--------------------

#. We need to create a new directory in our repository, where we save our new template files. We can name it for example ``our_template``.
#. Create a new file called ``conf.json`` and store it in this new directory. The configuration file will specify, what is the output of the template and what is the base template. It should look like this:
    
    .. code-block:: json

        {
            "base_template": "pj",
            "mimetypes": {
                "text/html": true
            }
        }

#. Create a new file that will extend the Jinja template file from Pretty Jupyter. Name it for example ``index.html.j2`` and place it into ``our_template`` directory. The file should look like this:

    .. code-block:: jinja

        {%- extends "pj.index.html.j2" -%}

        ...

#. In the new ``index.html.j2`` file, override or extend some of the blocks to provide custom behavior. For example:

    .. code-block:: jinja

        {%- extends "pj.index.html.j2" -%}

        {% block notebooks_css %}
        {# call the super in this instance to apply default styles #}
        {{ super() }}

        <style>
            html {
                background-color: red;
            }
        </style>
        {% endblock notebook_css %}

.. important::
    The files, such as ``index.html.j2``, are Jinja template files. For more information about how they work, check out `its documentation <https://jinja.palletsprojects.com/>`_, specifically
    the sections about blocks and inheritance.


Exporting with Custom Template
--------------------------------

To export the Jupyter notebook using our newly created template, we need to change the basic export command a little bit:

.. code-block:: bash
    :caption: Code: Export with Custom Template

    jupyter nbconvert --to html --template custom_template --TemplateExporter.extra_template_basedirs=path/to/directory/w/our/custom/template /path/to/ipynb/file

Blocks
------------

Some of the most interesting that we can overide are:

* ``notebook_css``: Specify styling for your pages here. It is highly recommended to call ``super`` in this block to apply default styles as well.
* ``notebook_js``: Specify JavaScript for the pages here. It is highly recommended to call ``super``, otherwise the page might break.
* ``page_header``: We can provide a custom page header by overriding this block.
* ``main_container_start``: Start of the main container. Can be added to provide notebook-level logo etc.
* ``main_container_end``: End of the main container. Can be used for a footer.

Examples
----------

Check out Pretty Jupyter's `example repository <https://github.com/JanPalasek/pretty-jupyter-examples>`_, specifically:

* **extending-template**: This example shows how to customize the template. It overrides ``page_header`` and removes it and specifies the header inside ``main_container_start``. It also specifies a custom footer in ``main_container_end``.
