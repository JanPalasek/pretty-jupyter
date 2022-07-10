# Pretty Jupyter
![Build](https://github.com/JanPalasek/pretty-jupyter/actions/workflows/ci.yml/badge.svg)

Pretty Jupyter is a package that creates beautifully styled and dynamic html webpage from Jupyter notebook. Check it yourself in our [demo](http://janpalasek.com/pretty-jupyter-example.html) and compare it with the [default jupyter](http://janpalasek.com/classic-jupyter-example.html).

All it takes to generate the output webpage are two simple commands, see [installation](https://github.com/JanPalasek/pretty-jupyter#installation) and [usage](https://github.com/JanPalasek/pretty-jupyter#usage).

<img src="docs/demo.gif" alt="demo preview" width=70% />

## Main Features

- :point_right: Visually appealing styles.
- :point_right: Automatic table of content's generation.
- :point_right: Tabsets.
- :point_right: Using Python variables in Markdown.
- :point_right: Code folding.

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

- [Documentation for Pretty Jupyter](https://github.com/JanPalasek/pretty-jupyter/wiki).
- [Examples](https://github.com/JanPalasek/pretty-jupyter-examples).

## Dev Installation
```sh
git clone https://github.com/JanPalasek/pretty-jupyter.git
cd pretty-jupyter
./env/install.ps1 # Or sh env/install.sh on linux
```

## Credits

Credits for styles, toc, tabs etc. go to developers of RMarkdown and its packages. A big part of this project is applying their incredible work to Jupyter. Credits also belong to `nbconvert` project.
