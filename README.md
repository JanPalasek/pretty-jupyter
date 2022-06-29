# Pretty Jupyter
![Build](https://github.com/JanPalasek/pretty-jupyter/actions/workflows/ci.yml/badge.svg)

Pretty Jupyter generates beautifully styled and dynamic html from ipynb notebook.

It takes the input ipynb notebook, transforms it into html and additionally handles:

- Automatic advanced table of content's generating.
- Simple utilization of tabsets.
- Applies prettier styling.
- And more in the future.

See yourself:

[Classic Jupyter](http://janpalasek.com/classic-jupyter-example.html) versus [Pretty Jupyter](http://janpalasek.com/pretty-jupyter-example.html)

## Installation
Requires:
- Python 3: it's been tested for versions 3.6, 3.7, 3.8, 3.9, but it most likely works for many more.

```powershell
python -m pip install pretty-jupyter
```

## Usage

Use [nbconvert](https://github.com/jupyter/nbconvert) with template pj (pretty-jupyter) to generate the html report with new styles.

```powershell
jupyter nbconvert --to html --template pj ${PATH_TO_IPYNB}
```

## Dev Installation
```sh
git clone https://github.com/JanPalasek/pretty-jupyter.git
cd pretty-jupyter
./env/install.ps1 # Or ./env/install.sh on linux
```

## Credits

Credits for styles, toc, tabs etc. go to developers of RMarkdown and its packages. A big part of this project is applying their incredible work to Jupyter.
