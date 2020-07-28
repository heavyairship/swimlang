import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_lang",
    version="0.0.1",
    author="Andrew Fichman",
    description="Simple Functional Programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/heavyairship/SimpleLang",
    packages=['simple_lang'],
    package_dir={'simple_lang': 'simple_lang'},
    package_data={'simple_lang': []},
    python_requires='>=3.6',
)
