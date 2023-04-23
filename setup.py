# setup file

import setuptools
setuptools.setup(
    name="summalarva",
    version="0.0.1",
    author="nhannht",
    author_email="nhanclassroom@gmail.com",
    description="A package for summarizing documents",
    packages=setuptools.find_packages(),
    install_requires=[
        "rich",
        "cohere",
        "pdfminer.six",
        "requests",
        "tiktoken"
    ],
    scripts=["summalarva/summarize_pdf.py"],
    python_requires='>=3.6',
)




