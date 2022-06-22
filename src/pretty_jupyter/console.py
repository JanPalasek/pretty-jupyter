import os
import shutil
import subprocess
import sys
import click
from traitlets.config import Config
from nbconvert.exporters import HTMLExporter
import pkg_resources
from pathlib import Path


@click.command()
@click.argument("input", type=click.Path())
@click.option("--out", default=None, type=click.Path())
@click.option("--include-input/--exclude-input", default=False)
def nbconvert(input, out, include_input):
    """
    Takes the .ipynb notebook from the INPUT and transforms it into HTML.
    Note that after installing you can also use jupyter nbconvert directly.
    """
    if out is None:
        out = os.path.join(os.path.dirname(input), f"{Path(input).stem}.html")

    config =  Config()
    config.HTMLExporter.template_name = "rmd"
    config.HTMLExporter.extra_template_basedirs = pkg_resources.resource_filename("pretty_jupyter", "templates")
    config.HTMLExporter.exclude_input = not include_input

    exporter = HTMLExporter(config)
    with open(input, "r", encoding="utf-8") as file:
        res = exporter.from_file(file)

    with open(out, "w", encoding="utf-8") as file:
        file.write(res[0])

@click.command()
def install():
    """
    Installs this package and makes it callable by `jupyter nbconvert` without the need to specify extra_template_basedirs.
    """
    src_folder = pkg_resources.resource_filename("pretty_jupyter", "templates")
    target_folder = os.path.join(sys.prefix, "share/jupyter/nbconvert/templates")
    shutil.copytree(src_folder, target_folder, dirs_exist_ok=True)


@click.version_option()
@click.group()
def cli():
    pass

cli.add_command(nbconvert)
cli.add_command(install)