import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nlp_synt_data",
    packages=["nlp_synt_data"],
    install_requires=['pandas'],
    version="0.0.9",
    author="Tommaso Romano'",
    author_email="romabob1300@gmail.com",
    description="Synthesized Data for NLP Tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tommasoromano/nlp-synt-data",
    license="The MIT License (MIT)",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)