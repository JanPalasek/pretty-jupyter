Changelog
============================

2.0.0-rc0
------------

- Implemented cell and notebook-level metadata.
- Changed design, added the old one to pj-legacy template.
    - This required changing of the structure of jinja template a bit.
- Updated documentation, added section for metadata, modified existing bits.
- Allowed to specify classes for any Markdown / HTML element.
- Changed tokens convention (tabset -> .tabset). It is still backwards compatible though.
- Implemented script that creates basic ipynb document with Pretty Jupyter basic elements (title,...).
- Switched from setup.py to setup.cfg and pyproject.toml.
- Added detailed selenium tests for notebooks generating.
