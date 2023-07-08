import base64
from io import BytesIO

_MARKDOWN_SUPPORTED_FMT_MAP = {"png": "png", "jpeg": "jpeg", "jpg": "jpeg"}
_MARKDOWN_IMG_FORMAT = r"![image](data:image/{format};base64,{encoded})"

_HTML_SUPPORTED_FMT_MAP = {"svg": "svg+xml", "png": "png", "jpeg": "jpeg", "jpg": "jpeg"}
_HTML_IMG_FORMAT = r"<img src='data:image/{format};base64,{encoded}' />"


def matplotlib_fig_to_markdown(fig, fmt="png", autoclose: bool = True, bbox_inches: str = "tight"):
    """
    Converts matplotlib figure to embedded markdown image.

    Args:
        fig: Matplotlib figure.
        fmt (str, optional): Format of the output image. Supported values are: png and jpg. Defaults to "png".
        autoclose (bool): If true, then matplotlib global plot is closed. This prevents it from being flushed by Jupyter notebook. Defaults to True.
        bbox_inches (str): Parameter sent to savefig. Defaults to "tight".

    Returns:
        str: Markdown string embedded representation of the figure.
    """
    return convert_mpl(
        fig,
        fmt=fmt,
        output_fmt_string=_MARKDOWN_IMG_FORMAT,
        supported_fmt_map=_MARKDOWN_SUPPORTED_FMT_MAP,
        autoclose=autoclose,
        bbox_inches=bbox_inches,
    )


def matplotlib_fig_to_html(fig, fmt="png", autoclose: bool = True, bbox_inches: str = "tight"):
    """
    Converts matplotlib figure to embedded html image.

    Args:
        fig: Matplotlib figure.
        fmt (str, optional): Format of the output image. Supported values are: png, jpg and svg. Defaults to "png".
        autoclose (bool): If true, then matplotlib global plot is closed. This prevents it from being flushed by Jupyter notebook. Defaults to True.
        bbox_inches (str): Parameter sent to savefig. Defaults to "tight".

    Returns:
        str: Markdown string embedded representation of the figure.
    """
    return convert_mpl(fig, fmt, _HTML_IMG_FORMAT, _HTML_SUPPORTED_FMT_MAP, autoclose, bbox_inches)


def convert_mpl(
    fig,
    fmt,
    output_fmt_string,
    supported_fmt_map,
    autoclose: bool = True,
    bbox_inches: str = "tight",
):
    """
    Converts matplotlib figure into embedded inline string.

    Args:
        fig: Matplotlib figure.
        fmt (str): Format of the output (png, jpg,...).
        output_fmt_string (str): String format of the output. It must have two empty format strings to specify, where one is named format and the second is named encoded.
        supported_fmt_map (dict): Maps supported formats to the format used in the.
        autoclose (bool): If true, then matplotlib global plot is closed. This prevents it from being flushed by Jupyter notebook. Defaults to True.
        bbox_inches (str): Parameter sent to savefig. Defaults to "tight".

    Returns:
        str: Returns string representation of the figure.
    """
    if fmt not in supported_fmt_map:
        raise ValueError("Format '{format}' is currently not supported.")

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format=fmt, bbox_inches=bbox_inches)

    markdown = output_fmt_string.format(
        format=supported_fmt_map[fmt], encoded=base64.b64encode(tmpfile.getvalue()).decode("utf-8")
    )

    if autoclose:
        import matplotlib.pyplot as plt

        plt.close()
    return markdown
