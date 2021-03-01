import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="flowbase",
    version="0.0.3",
    description="Python implementation of the FlowBase Flow-based Programming micro-framework idea (see flowbase.org)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Samuel Lampa",
    author_email="samuel.lampa@rilnet.com",
    url="https://github.com/flowbase/flowbase-python",
    license="MIT",
    keywords="flow-based programming",
    packages=["flowbase",],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ],
)
