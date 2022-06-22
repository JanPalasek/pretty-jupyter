from pretty_jupyter._preprocessors import TokenPreprocessor
from pretty_jupyter.__magics import JinjaMagics

__all__ = [
    "TokenPreprocessor",
    "JinjaMagics"
]

def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    ipython.register_magics(JinjaMagics)