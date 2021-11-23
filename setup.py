import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vws",
    version="0.0.1",
    author="vinhpx",
    author_email="phamxuanvinh023@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sudo-VP/Vietnamese-Word-Segmentation-Python",
    project_urls={
        "Bug Tracker": "https://github.com/Sudo-VP/Vietnamese-Word-Segmentation-Python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "vws"},
    packages=setuptools.find_packages(where="vws"),
    python_requires=">=3.6",
)