import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-automapper",
    version="0.0.1",
    author="Andrii Nikolaienko",
    author_email="anikolaienko14@gmail.com",
    description="Library for automatically mapping one object to another",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anikolaienko/py-automapper",
    project_urls={
        "Bug Tracker": "https://github.com/anikolaienko/py-automapper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)