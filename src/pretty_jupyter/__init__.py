from pretty_jupyter.magics import JinjaMagics

# these imports are here for conf.json to work
from pretty_jupyter.preprocessors import TokenPreprocessor, RemoveInputPreprocessor, RemoveOutputPreprocessor

def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    ipython.register_magics(JinjaMagics)
