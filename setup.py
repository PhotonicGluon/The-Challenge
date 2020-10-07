"""
setup.py

Created on 2020-09-19
Updated on 2020-10-07
"""

from setuptools import find_packages, setup

from the_challenge import __version__

setup(
    name="The-Challenge",
    version=__version__,
    description=" A Web Project About Solving Mathematics Problems",
    author="Ryan Kan",
    author_email="ryankanok@gmail.com",
    url="https://github.com/Ryan-Kan/The-Challenge",
    python_requires='~=3.8',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[x.strip() for x in open("requirements.txt", "r").readlines()],
    entry_points={
        "console_scripts": [
            "update_the_challenge=the_challenge.command_line:update_the_challenge"
        ]
    }
)
