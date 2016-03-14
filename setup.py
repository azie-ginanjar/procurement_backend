from setuptools import find_packages
from setuptools import setup

from itgetlink.backend import __version__

with open("README.rst") as f:
    long_desc = f.read()

setup(
    name="itgetlink.backend",
    version=__version__,
    description="Handles Authentication",
    long_description=long_desc,
    author="IT-Getlink",
    url="",
    packages=find_packages(),
    license="Proprietary",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.4",
    ],
    entry_points={
        "console_scripts": ["itGetlink-procurement=itgetlink.backend.factory:run_cli"],
    },
    zip_safe=False,
    install_requires=[
        "arrow",
        "blinker",
        "celery",
        "colander>=1.0b1",
        "dictalchemy",
        "flask-appconfig",
        "flask-migrate",
        "flask-script",
        "flask-sqlalchemy",
        "mimerender",
        "psycopg2",
        "raven",
        "requests",
        "six",
        "xmltodict",
        "flask-cors",
    ],
    include_package_data=True,


)
