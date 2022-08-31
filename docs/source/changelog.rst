Changelog
============================


2.0.0
-----------

- Added other themes and required.js directly to the report.
- Fixed an issue with weird characters ruining tabset and toc (characters like parentheses, braces, square brackets, #, ", ', etc)
- Fixed an issue where empty jinja markdown cell would lead to an error when running pretty jupyter
- Added ``code_tools`` to html output options to provide an option to enable / disable code tools. Default value is false.
- Implemented cell and notebook-level metadata.
- Changed design, added the old one to pj-legacy template.
    - This required changing of the structure of jinja template a bit.
- Updated documentation, added section for metadata, modified existing bits.
- Allowed to specify classes for any Markdown / HTML element.
- Changed tokens convention (tabset -> .tabset). It is still backwards compatible though.
- Implemented script that creates basic ipynb document with Pretty Jupyter basic elements (title,...).
- Switched from setup.py to setup.cfg and pyproject.toml.
- Added detailed selenium tests for notebooks generating.
