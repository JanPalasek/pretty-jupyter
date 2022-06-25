from IPython import display
from IPython.core.magic import Magics, magics_class, cell_magic
import jinja2

from pretty_jupyter.tokens import convert_markdown_tokens_to_html


@magics_class
class JinjaMagics(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        
        # create a jinja2 environment to use for rendering
        # this can be modified for desired effects (ie: using different variable syntax)
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))

        # possible output types
        self.display_functions = dict(html=display.HTML, 
                                      latex=display.Latex,
                                      json=display.JSON,
                                      pretty=display.Pretty,
                                      display=display.display,
                                      markdown=display.Markdown)

    @cell_magic
    def jinja(self, line, cell):
        display_fn_name = line.lower().strip()
        if display_fn_name not in self.display_functions:
            raise ValueError(f"Unknown parameter {display_fn_name}.")

        display_fn = self.display_functions.get(display_fn_name)

        # render the cell with jinja (substitutes variables,...)
        tmp = self.env.from_string(cell)
        rend = tmp.render(dict((k,v) for (k,v) in self.shell.user_ns.items() 
                                        if not k.startswith('_') and k not in self.shell.user_ns_hidden))
        
        # convert tokens to html
        rend = convert_markdown_tokens_to_html(rend)

        # display markdown
        return display_fn(rend)