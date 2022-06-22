import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pretty-jupyter',
    author="Jan Palasek",
    version='0.1a',
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={
        "": "src"
    },
    install_requires=[
        "click",
        "jupyter",
        "nbconvert"
    ],
    packages=setuptools.find_packages("src"),
    include_package_data=True,
    entry_points={
        "console_scripts": ["pretty-jupyter = pretty_jupyter.__main__:cli"]
    },
    python_requires=">=3.6"
)
