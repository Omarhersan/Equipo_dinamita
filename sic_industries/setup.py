import os
import datetime as dt
import logging
from setuptools import setup, find_packages


uname = "unknown"
try:
    uname = os.getlogin()
except Exception:
    logging.warning("Failed to retrieve uname.")


with open("requirements.txt", "r") as file:
    requirements = [
        req.strip()
        for req in file.read().splitlines()
        if req and not req.startswith("#")
    ]


APP_NAME = "sic_industries"

setup(
    name=f"{APP_NAME}-{uname}-{dt.datetime.utcnow().isoformat()}",
    version="0.1.0",
    description="SIC Industries",
    package_dir={
        "": "src",
    },
    packages=find_packages(where="src"),
    install_requires=requirements,
)
