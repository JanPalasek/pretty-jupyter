<h1 align="center">
  <br>
  Pretty Jupyter
  </br>
</h1>
<h4 align="center">Simple package for beautiful & dynamic reports</h4>

<p align="center">
  <a href="https://github.com/JanPalasek/pretty-jupyter/actions/workflows/ci.yml/badge.svg"><img src="https://github.com/JanPalasek/pretty-jupyter/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="https://img.shields.io/github/v/release/JanPalasek/pretty-jupyter"><img src="https://img.shields.io/github/v/release/JanPalasek/pretty-jupyter" /></a>
</p>

<p align="center">
  <img src="docs/demo.gif" alt="demo preview" width="70%" />
</p>

## Introduction

Pretty Jupyter is a package that creates beautifully styled and dynamic html webpage from Jupyter notebook.

Check out the **[demo](http://janpalasek.com/pretty-jupyter-example.html)** and compare it with the [default jupyter](http://janpalasek.com/classic-jupyter-example.html). You can try Pretty Jupyter [online](http://janpalasek.com/pretty-jupyter.html).

## Main Features

- :point_right: Visually appealing styles.
- :point_right: Automatic Table of Contents generation.
- :point_right: Tabsets.
- :point_right: Using Python variables in Markdown.
- :point_right: Code Folding.

All these features are integrated directly in the output html page. Therefore there is no need for an interpreter running in the backend.

## Installation

```sh
python -m pip install pretty-jupyter
```

## Usage

```sh
jupyter nbconvert --to html --template pj ${PATH_TO_IPYNB}
```

To unlock the full potential of Pretty Jupyter, see [the customization section](https://github.com/JanPalasek/pretty-jupyter/wiki/2.-Customization) in the documentation.

## Documentation

- [Documentation for Pretty Jupyter](https://github.com/JanPalasek/pretty-jupyter/wiki)
- [Examples](https://github.com/JanPalasek/pretty-jupyter-examples)

## Dev Installation
```sh
git clone https://github.com/JanPalasek/pretty-jupyter.git
cd pretty-jupyter
./env/install.ps1 # Or sh env/install.sh on linux
```

## Credits

Credits for styles, toc, tabs etc. go to developers of RMarkdown and its packages. A big part of this project is applying their incredible work to Jupyter. Credits also belong to `nbconvert` project.
