""":license: MIT, see LICENSE for more details."""

from setuptools import find_packages, setup

setup(
    long_description=open("README.md").read(),  # noqa: PTH123, SIM115
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3",
    ],
    url="https://github.com/aruba-uxi/celery-sqlalchemy-scheduler",
    packages=find_packages(exclude=["tests"]),
    package_data={"rdbbeat": ["py.typed"]},
    include_package_data=True,
    zip_safe=False,
)
