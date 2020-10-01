import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swimlang",
    version="0.0.1",
    author="Andrew Fichman",
    description="Simple functional programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/heavyairship/swimlang",
    packages=['swimlang'],
    package_dir={'swimlang': 'swimlang'},
    package_data={'swimlang': []},
    python_requires='>=3.6',
)
