"""
setup.py

Created on 2020-09-19
Updated on 2020-09-19
"""

from setuptools import find_packages, setup

setup(
    name="The-Challenge",
    version="1.0.0a1.dev1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
)
