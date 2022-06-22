from IPython import display
from IPython.core.magic import Magics, magics_class, cell_magic
import jinja2

@magics_class
class JinjaMagics(Magics):
    """
    A class which enables us to use jinja magics in the code cell and write e.g. markdown with substituted variables etc.

    Src: https://gist.github.com/schuster-rainer/cccdab4877a90fba35f5
    """
    
    def __init__(self, shell):
        super(JinjaMagics, self).__init__(shell)
        
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
        '''
        jinja2 cell magic function.  Contents of cell are rendered by jinja2, and 
        the line can be used to specify output type.

        Example:

        Assume we have a value stored in the variable "a".
        ```python
        %%jinja markdown

        We can print the value in the variable *a* as simple as this: {{ a }}!.
        ```
        '''
        f = self.display_functions.get(line.lower().strip(), display.display)
        
        tmp = self.env.from_string(cell)
        rend = tmp.render(dict((k,v) for (k,v) in self.shell.user_ns.items() 
                                        if not k.startswith('_') and k not in self.shell.user_ns_hidden))
        
        return f(rend)
