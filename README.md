# Pretty Jupyter
![Build](https://github.com/JanPalasek/pretty-jupyter/actions/workflows/ci.yml/badge.svg)

Are you tired of everyone saying that the reports from R are prettier? Fear no more!

Pretty jupyter package takes the input ipynb notebook, transforms it into html and applies RMarkdown styles, taking its all advantage while being able to code in Python. Upon that, it also provides useful functionality, such as combining markdown and code etc.

See yourself:

[Classic jupyter](http://janpalasek.com/classic-jupyter-example.html) versus [Pretty Jupyter](http://janpalasek.com/pretty-jupyter-example.html)

## Installation
### As a Package

1. Install the package from GitHub
    ```powershell
    python -m pip install git+https://github.com/JanPalasek/pretty-jupyter
    ```

2. Run the install command.
    ```
    pretty-jupyter install
    ```


### As a Repository

**Prerequisities**
- Python: 3.8

1. Clone the project and go to its root directory.
    ```powershell
    git clone https://github.com/JanPalasek/pretty-jupyter
    cd pretty-jupyter
    ```
2. Run the installation
    ```sh
    ./env/install.ps1 # or ./env/install.sh on linux (currently untested)
    ```

## Generating HTML

After installation, the running of the pretty jupyter is simple. Just invoke the following command:

```powershell
jupyter nbconvert --to html --template rmd ${PATH_TO_IPYNB}
```

For example try the following from the root of this repository: `jupyter nbconvert --to html --template rmd tests/fixture/basic.ipynb`
This invokes the base command from `nbconvert` package, but instead of applying the default template, it applies rmd template from pretty-jupyter.

Some notables parameters, you might want to use:

- `--no-input`: Hides input cells.

To fill the title, edit the notebook metadata and fill in title property in json, as you normally would.

## Advanced Functionality

### Tabset
1. Define a markdown header, whose sub-headers will be tabs.
2. Write the following string on the line right under the header: `[//]: <> (-.- tabset)`.
3. Profit.

Example:
```md
## Tabset
[//]: <> (-.- tabset)

### Tab 1

This is the first tag.

### Tab 2

This is the second tab.
```

### Variables in Markdown
Printing code variables into Markdown would be useful, however the basic jupyter does not support this. For Jupyter, there is an [extension](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/python-markdown/readme.html) that allows us to use code in markdown cells. However this cannot be afaik use in Jupyter Lab.

To overcome this obstacle, we can use Jinja.

First we need to include pretty_jupyter magics by using the following line.

```python
%load_ext pretty_jupyter
```

Then, in code cells, we can write markdown combined with jupyter:

```python
# code cell defining variable a with value that we will use in the next code cell
a = 10
```

```jinja
%%jinja markdown

We can write markdown like this and print the value in variable a as simply as this: {{ a }}.
```

Note that its output will be automatically hidden. This can be overidden by specifying using parameter when calling nbconvert: `--RemoveInputPreprocessor.jmarkdown=0`.


## Credits

All credits for styles, toc, tabs etc. go to developers of RMarkdown and its packages. This project just applies their incredible work to Jupyter.
