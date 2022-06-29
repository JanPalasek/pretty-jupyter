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
@click.option("--include-input/--exclude-input", default=True)
def nbconvert(input, out, include_input):
    """
    Takes the .ipynb notebook from the INPUT and transforms it into HTML.
    Note that after installing you can also use jupyter nbconvert directly.
    """
    if out is None:
        out = os.path.join(os.path.dirname(input), f"{Path(input).stem}.html")

    config =  Config()
    config.HTMLExporter.template_name = "pj"
    config.HTMLExporter.extra_template_basedirs = [pkg_resources.resource_filename("pretty_jupyter", "templates")]
    config.HTMLExporter.exclude_input = not include_input

    exporter = HTMLExporter(config)
    with open(input, "r", encoding="utf-8") as file:
        res = exporter.from_file(file)

    with open(out, "w", encoding="utf-8") as file:
        file.write(res[0])


@click.version_option()
@click.group()
def cli():
    pass

cli.add_command(nbconvert)
