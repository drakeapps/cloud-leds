import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudlights", # Replace with your own username
    version="1.0.0",
    author="James Wilson",
    author_email="james@drakeapps.com",
    description="LED Strip Controller Class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/drakeapps/cloud-leds",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)