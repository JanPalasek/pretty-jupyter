import setuptools
import glob


with open("README.md", "r") as fh:
    long_description = fh.read()

data_files = []
data_files.append(
    ("share/jupyter/nbconvert/templates/pj",
        list(glob.glob('src/pretty_jupyter/templates/pj/*.j2'))
        + ["src/pretty_jupyter/templates/pj/conf.json"])
)
data_files.append(
    ("share/jupyter/nbconvert/templates/pj/static",
        list(glob.glob("src/pretty_jupyter/templates/static/*")))
)

setuptools.setup(
    name='pretty-jupyter',
    author="Jan Palasek",
    version='0.1b1',
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={
        "": "src"
    },
    install_requires=[
        "click",
        "ipython",
        "nbconvert"
    ],
    packages=setuptools.find_packages("src"),
    include_package_data=True,
    data_files=data_files,
    entry_points={
        "console_scripts": ["pretty-jupyter = pretty_jupyter.__main__:cli"]
    }
)
