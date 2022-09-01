Quick Start
=========================

Installation
-----------------

Pretty Jupyter can be installed by using the following command:

.. code-block:: bash

    pip install pretty-jupyter


Creating Our First Pretty Notebook
-------------------------------------

Using Pretty Jupyter is pretty much identical to using normal Jupyter. We will work through a simple example to demonstrate this.

To start, we can create a new notebook it "my-first-notebook.ipynb". To simplify the start, Pretty Jupyter provides a custom command for this purpose.

.. code-block:: bash

    pretty-jupyter quickstart "my-first-notebook.ipynb"

The initial notebook contains two cells: raw cell and a code cell. Raw cell contains YAML header that specifies notebook's metadata. The code cell loads Pretty Jupyter magics into the notebook and allows us to use its features.

We can edit the values of the YAML header and provide e.g. a custom title for the page.

.. code-block:: yaml

    title: Our Notebook Title
    author: Developer
    date: "{{ datetime.now().strftime('%Y-%m-%d %H:%M:%S') }}"

.. code-block:: python

    # load pretty jupyter's magics
    %load_ext pretty_jupyter

We can edit the values in the YAML header and provide e.g. our custom title for the page.

Next we can fill in the next Jupyter's code cells as following.

.. code-block:: python

    # import packages
    import pandas as pd

.. code-block:: markdown

    %%jmd

    ## First Section

    This is our first section. We use so called **Jinja Markdown** here.
    It allows us to combine Markdown with Python variables and makes
    for a more dynamic report.

    We can for example print pandas version such as this: {{ pd.__version__ }}.

.. code-block:: python

    # we create a simple dataframe for demonstration purposes
    data = pd.DataFrame({"col1": [1, 2, 3, 4], "col2": ["cat1", "cat2", "cat1", "cat2"]})

    data.head()

.. code-block:: markdown

    %%jmd

    ## Tabset Root
    [//]: # (-.- .tabset .tabset-pills)

    The content of this section will be shown as tabs. This will help us avoid potential scrolling and improve the HTML UI.

    ### First Tab
    In the first tab, we can show some graphs or tables. We can output the table like this:

    {{ data.head().to_html() }}

    ### Second Tab
    In the second tab, we can do the same. Btw maths also works in the tabs.

    ## Not a Tabset
    This section will not be tabbed because it has the same level (or higher) as the Tabset Root.


Exporting the Notebook
--------------------------

Now we can use Pretty Jupyter to generate the result HTML report. To do this, use the following command:

.. code-block::

    jupyter nbconvert --to html --template pj /path/to/ipynb/file

.. seealso::
    Pretty Jupyter uses nbconvert's underhood including its command line interface. Check out `its documentation <https://nbconvert.readthedocs.io/>`_.

It generates the output HTML file to the same directory as the input file.

Next Steps
---------------

Check out other pages from Getting Started section in this documentation.
Also check out our `example repository <https://github.com/JanPalasek/pretty-jupyter-examples>`_. It contains a lot of use-cases and demonstrations, how to use Pretty Jupyter.