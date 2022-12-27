# Inspired by:
# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/

import codecs
import os
import re

from setuptools import find_packages, setup

###################################################################

NAME = "cv"
PACKAGES = find_packages(where="cv")
META_PATH = os.path.join("cv", "scripts", "__init__.py")
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Unix",
    "Operating System :: MacOS",
    "Programming Language :: Python",
    "Topic :: Text Processing :: Markup :: LaTeX",
]
INSTALL_REQUIRES = ["pandas", "numpy", "gsheets", "ads", "beautifulsoup4"]

###################################################################

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=find_meta("uri"),
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        package_data={"": ["README.md", "LICENSE"]},
        long_description=read("README.md"),
        long_description_content_type="text/x-rst",
        packages=PACKAGES,
        package_dir={"": "cv"},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        options={"bdist_wheel": {"universal": "1"}},
    )
