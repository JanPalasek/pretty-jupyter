Getting Started
=========================

Installation
-----------------

Pretty Jupyter can be installed by using the following command:

.. code-block:: bash

    pip install pretty-jupyter


Creating Our First Pretty Notebook
-------------------------------------

Using Pretty Jupyter is pretty much identical to using normal Jupyter. We will work through a simple example to demonstrate this.

To start, create an empty Jupyter Notebook file and start filling it with the following content. For purposes of this tutorial, name it "my-first-notebook.ipynb".

.. code-block:: bash

    # load Pretty Jupyter features
    %load_ext pretty_jupyter

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
    [//]: <> (-.- tabset tabset-pills)

    The content of this section will be shown as tabs. This will help us avoid potential scrolling and improve the HTML UI.

    ### First Tab
    In the first tab, we can show some graphs or tables. We can output the table like this:

    {{ data.head().to_html() }}

    ### Second Tab
    In the second tab, we can do the same. Btw maths also works in the tabs.

    ## Not a Tabset
    This section will not be tabbed because it has the same level (or higher) as the Tabset Root.

At last, we will set our page title. It is by default set to the name of the file, which is not what we want. To override this behavior, we specify ``"title"`` attribute in the notebook's metadata.

.. note::
    Some environments, such as JupyterLab and Jupyter, support specifying notebook metadata in their UI.
    
    In others, we need to open the notebook file as a text, locate "metadata" attribute in its json and write the title there directly.


Exporting the Notebook
--------------------------

Now we can use Pretty Jupyter to generate the result HTML report. To do this, use the following command:

.. code-block::

    jupyter nbconvert --to html --template pj /path/to/ipynb/file

.. seealso::
    Pretty Jupyter uses nbconvert's underhood including its command line interface. Check out `its documentation <https://nbconvert.readthedocs.io/>`_.

It generates the output HTML file to the same directory as was the input file.

Next Steps
---------------

For a more in-depth tutorials, check out our `example repository <https://github.com/JanPalasek/pretty-jupyter-examples>`_. You might even find your use-case there. Also, check out the other sections of the User Documentation.