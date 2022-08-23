Jinja Markdown
===================

Imagine the simplest scenario: You want to output a mean of a column in your report. The natural way would be to write a markdown and then
insert your variable in it in a proper place. This would allow a seamless integration between the text and the code.
However, standard Jupyter notebooks do not allow us to use Markdown with Python code variables in one cell.

Pretty Jupyter aims to solve this by **Jinja Markdown.** To demonstrate this, try the following example in your own notebook:

.. code-block:: python
    
    # load pretty jupyter
    %load_ext pretty_jupyter


.. code-block:: python

    # define a variable in a normal cell
    a = 10

.. code-block:: markdown

    %%jinja markdown

    We wrote `%%jinja markdown` on the first line and this transforms the code cell into a Jinja Markdown cell.

    Now we seamlessly combine Python variable "a" from before as simple as this: {{ a }}.

.. important::
    Instead of ``%%jinja markdown``, we can write ``%%jmd`` as a shortcut.

.. note::
    Jinja Markdown internally uses Jinja templating engine. Each cell is fed separately to the engine together with the local variables (and imports).
    Check out `Jinja documentation <https://jinja.palletsprojects.com/>`_ to unlock its full power.

Jinja allows us to customize the way we print the output using its feature called filters. Using this, we can e.g. round the float. For example:

.. code-block:: markdown

    %%jinja markdown

    An example of rounding: {{ (10 / 3) | round(2) }}

.. warning::
    We cannot use Python keywords directly in Jinja because Jinja is technically a different language. An example of such keywords could be
    ``lambda``, ``int`` (for conversions) etc. In most of cases, this can be easily bypassed by using named functions instead or Jinja filters.


Variables with HTML
------------------------

The variables that we print do not have to be a simple integer or float types. We can print any HTML like this!

An example below demonstrates this capabilities for tables:

.. code-block:: python

    %load_ext pretty_jupyter

    import pandas as pd

    d = pd.DataFrame({"a": [1, 2, 3])

.. code-block:: markdown

    %%jmd
    <details>
    <summary>Table</summary>

    {{ d.head().to_html() }}

    </details>

The similar thing can be done with plots. We just need to transform them from objects to HTML.

.. code-block:: python
    
    %load_ext pretty_jupyter

    import matplotlib.pyplot as plt
    from pretty_jupyter.helpers import matplotlib_fig_to_html

.. code-block:: markdown
    
    %%jmd

    {{ matplotlib_fig_to_html(plt.plot([1, 2], [3, 4])[0].figure) }}


Examples
--------------------

Check out our `example repository <https://github.com/JanPalasek/pretty-jupyter-examples>`_ for this and more examples. Specifically:

* **main-features-demo**: Has a section on Jinja Markdown. It demonstrates how to use it with matplotlib and plotly.
* **dynamic-tabsets**: Demonstrates, how to dynamically create tabsets using Jinja Markdown.
* **interactive-components**: Demonstrates, how to use interactive components with Pretty Jupyter, such as plotly or itables (interactive tables). In short, it works as with normal Jupyter.