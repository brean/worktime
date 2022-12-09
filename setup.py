#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('worktime/data')


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="worktime",
    description="Work time overview application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brean/worktime",
    version="0.1",
    license="Apache-2.0",
    author="Andreas Bresser",
    packages=find_packages(),
    tests_require=[],
    include_package_data=True,
    package_data={'': extra_files},
    install_requires=[
        'argcomplete',
        'jinja2',
        'caldav',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'worktime = worktime.cli:main',
        ],
    },
)
