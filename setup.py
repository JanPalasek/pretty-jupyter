import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pretty-jupyter',
    author="Jan Palasek",
    version='0.1b',
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
    entry_points={
        "console_scripts": ["pretty-jupyter = pretty_jupyter.__main__:cli"]
    }
)
