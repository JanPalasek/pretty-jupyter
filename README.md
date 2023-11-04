<h1 align="center">
  <br>
  Pretty Jupyter
  </br>
</h1>
<h4 align="center">Simple package for beautiful & dynamic reports</h4>

<p align="center">
  <a href="https://github.com/JanPalasek/pretty-jupyter/actions/workflows/ci.yml"><img src="https://github.com/JanPalasek/pretty-jupyter/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="https://pypi.org/project/pretty-jupyter/"><img src="https://img.shields.io/github/v/release/JanPalasek/pretty-jupyter" /></a>
  <a href='https://pretty-jupyter.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/pretty-jupyter/badge/?version=latest' alt='Documentation Status' />
</a>
</p>

<p align="center">
  <img src="docs/demo.gif" alt="demo preview" />
</p>

## Introduction

Pretty Jupyter is a package that creates beautifully styled and dynamic html webpage from Jupyter notebook.

Check out the **[demo](https://janpalasek.com/projects/pretty-jupyter/pretty-jupyter-example.html)** and compare it with the [default jupyter](https://janpalasek.com/projects/pretty-jupyter/classic-jupyter-example.html).

## Main Features

- :point_right: **Visually appealing styles**.
- :point_right: **Table of Contents** can be automatically generated.
- :point_right: Using **Python variables in Markdown**.
- :point_right: **Tabsets** for hiding section content behind clickable tabs.
- :point_right: **Code Folding**: Show/Hide code to filter out unnecessary content.
- :point_right: **Themes**: Selection from a wide variaty of available themes.
- :point_right: **Wide range of configuration options** with sensible defaults.
- :point_right: **Unobtrusive syntax** that works well in notebook environments.

All these features are integrated directly in the output html page. Therefore there is no need for an interpreter running in the backend.

## Installation

```sh
pip install pretty-jupyter
```

## Usage

```sh
jupyter nbconvert --to html --template pj /path/to/ipynb/file
```

## Resources

- **[Documentation](https://pretty-jupyter.readthedocs.io/)**
- **[Examples](https://github.com/JanPalasek/pretty-jupyter-examples)**
- **[Cheat Sheet](docs/cheatsheet/cheatsheet.pdf)**

## Credits

* **RMarkdown**: RMarkdown served as a great inspiration when making this package.
* **nbconvert**: Pretty Jupyter uses nbconvert underhood. Its great extendability allowed this project to be created.
