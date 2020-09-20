"""
setup.py

Created on 2020-09-19
Updated on 2020-09-20
"""

from setuptools import find_packages, setup

setup(
    name="The-Challenge",
    version=open("VERSION", "r").read().strip(),
    description=" A Web Project About Solving Mathematics Problems",
    author="Ryan Kan",
    author_email="ryankanonnkit@gmail.com",
    project_url={"Source Code": "https://github.com/Ryan-Kan/The-Challenge"},
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[x.strip() for x in open("requirements.txt", "r").readlines()]
)
