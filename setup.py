import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

# this is done only to copy to the nbconvert's expected target directory
# so 'jupyter nbconvert' recognizes our new template
data_files = []
data_files.append(
    ("share/jupyter/nbconvert/templates/pj", [
        "src/pretty_jupyter/templates/pj/conf.json",
        "src/pretty_jupyter/templates/pj/index.html.j2",
        "src/pretty_jupyter/templates/pj/base.html.j2"])
)
data_files.append(
    ("share/jupyter/nbconvert/templates/pj/static", [
        "src/pretty_jupyter/templates/pj/static/pj.js",
        "src/pretty_jupyter/templates/pj/static/pj.css"
    ])
)

setuptools.setup(
    name='pretty-jupyter',
    author="Jan Palasek",
    version='1.2.3',
    description="Export Jupyter notebook into beautiful and dynamic HTML report.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={
        "": "src"
    },
    install_requires=[
        "click",
        "ipython>=7.1",
        "nbconvert>=6.0",
        "jinja2>=3.0",
        "ipython-genutils>=0.1"
    ],
    packages=setuptools.find_packages("src"),
    include_package_data=True,
    data_files=data_files,
    entry_points={
        "console_scripts": ["pretty-jupyter = pretty_jupyter.__main__:cli"]
    },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Framework :: Jupyter',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9'
          ],
)
