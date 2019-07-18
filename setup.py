import setuptools


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_text = f.read()
    
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip()]
    
# read the __version__ variable from qubovert/_version.py
exec(open("qSonify/_version.py").read())


setuptools.setup(
    name="qSonify",
    version=__version__,
    author="Joseph Iosue",
    author_email="joe.iosue@yahoo.com",
    description="A package for sonifying quantum algorithms",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jiosue/qsonify",
    license=license_text,
    packages=setuptools.find_packages(exclude=("tests", "docs")),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
