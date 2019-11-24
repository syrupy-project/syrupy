import os
import sys

from setuptools import setup

python_requires = "~=3.6"

if sys.version_info[0] == 2:
    raise Exception("Only python 3 supported.")


def readme() -> str:
    with open("README.md") as f:
        return f.read()


if __name__ == "__main__":
    setup(
        name="syrupy",
        description="PyTest Snapshot Test Utility",
        author="Top Hat Open Source",
        author_email="opensource@tophat.com",
        url="git@github.com:tophat/syrupy.git",
        long_description=readme(),
        long_description_content_type="text/markdown",
        use_scm_version={"write_to": "version.txt"},
        package_dir={"": "src"},
        packages=["syrupy"],
        py_modules=["syrupy"],
        zip_safe=False,
        install_requires=[],
        setup_requires=["setuptools_scm"],
        entry_points={"pytest11": ["syrupy = syrupy"]},
        python_requires=python_requires,
        classifiers=["Framework :: Pytest"],
    )
