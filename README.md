# Pretty Jupyter
![Build](https://github.com/JanPalasek/pretty-jupyter/actions/workflows/ci.yml/badge.svg)

Are you tired of your peers saying that the reports from R are prettier? Fear no more!

Pretty jupyter package takes the input ipynb notebook, transforms it into html and additionally handles:

- Automatic advanced table of content's generating.
- Simple utilization of tabsets.
- Applies prettier styling.
- And more in the future.

See yourself:

[Classic Jupyter](http://janpalasek.com/classic-jupyter-example.html) versus [Pretty Jupyter](http://janpalasek.com/pretty-jupyter-example.html)

## Installation
Requires:
- Python 3: it's been tested for versions 3.6, 3.7, 3.8, 3.9, but it most likely works for many more.

1. Install the package from GitHub
    ```powershell
    python -m pip install git+https://github.com/JanPalasek/pretty-jupyter
    ```

2. Run the install command.
    ```
    pretty-jupyter install
    ```

## Usage

Use [nbconvert](https://github.com/jupyter/nbconvert) with template pj (pretty-jupyter) to generate the html report with new styles.

```powershell
jupyter nbconvert --to html --template pj ${PATH_TO_IPYNB}
```

## Credits

Credits for styles, toc, tabs etc. go to developers of RMarkdown and its packages. A big part of this project is applying their incredible work to Jupyter.
