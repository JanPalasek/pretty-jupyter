import os
import shutil
import sys
from pathlib import Path

import click
import pkg_resources
from nbconvert.exporters import HTMLExporter, LatexExporter, PDFExporter
from traitlets.config import Config


@click.command()
@click.argument("out_path", type=click.Path())
def quickstart(out_path):
    in_path = pkg_resources.resource_filename(
        "pretty_jupyter", os.path.join("quickstart", "empty.ipynb")
    )

    with open(in_path, "r") as file_r, open(out_path, "w") as file_w:
        in_text = file_r.read()
        file_w.write(in_text)


@click.command("nbconvert-dev")
@click.argument("input", type=click.Path())
@click.option("--to", default="html", type=click.Choice(["html", "pdf", "latex"]))
@click.option("--out", default=None, type=click.Path())
@click.option("--include-input/--exclude-input", default=True)
def nbconvert_dev(input, to, out, include_input):
    """
    Takes the .ipynb notebook from the INPUT and transforms it into HTML.
    Note that after installing you can also use jupyter nbconvert directly.
    """
    if out is None:
        out = os.path.join(os.path.dirname(input), f"{Path(input).stem}.{to}")

    template_map = {"html": "pj", "pdf": "pj-pdf", "latex": "pj-pdf"}

    config = Config()
    config.TemplateExporter.template_name = template_map[to]
    config.TemplateExporter.extra_template_basedirs = [
        pkg_resources.resource_filename("pretty_jupyter", "templates")
    ]
    config.TemplateExporter.exclude_input = not include_input

    if to == "html":
        exporter = HTMLExporter(config)
    elif to == "pdf":
        exporter = PDFExporter(config)
    elif to == "latex":
        exporter = LatexExporter(config)
    else:
        raise ValueError()

    with open(input, "r", encoding="utf-8") as file:
        res = exporter.from_file(file)
    output_data = res[0]

    # open file as bytes if the output data are bytes, otherwise opne it as a string
    file = open(out, "wb") if isinstance(output_data, bytes) else open(out, "w", encoding="utf-8")
    try:
        file.write(output_data)
    finally:
        file.close()


@click.command("install-dev")
def install_dev():
    """
    Installs this package and makes it callable by `jupyter nbconvert` without the need to specify extra_template_basedirs.
    """
    src_templates = ["pj", "pj-pdf", "pj-legacy"]

    for src_template in src_templates:
        src_folder = os.path.join(
            pkg_resources.resource_filename("pretty_jupyter", "templates"), src_template
        )
        target_folder = os.path.join(
            sys.prefix, f"share/jupyter/nbconvert/templates/{src_template}"
        )

        # for backward compatibility, otherwise copytree has dirs_exist_ok param
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
        shutil.copytree(src_folder, target_folder)


@click.version_option()
@click.group()
def cli():
    pass


cli.add_command(quickstart)
cli.add_command(nbconvert_dev)
cli.add_command(install_dev)
