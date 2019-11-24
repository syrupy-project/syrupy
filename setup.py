import os
import sys

from setuptools import setup

python_requires = "~=3.6"

if sys.version_info[0] == 2:
    raise Exception("Only python 3 supported.")

if __name__ == "__main__":
    setup(
        name="syrupy",
        description="PyTest Snapshot Test Utility",
        author="Top Hat Open Source",
        use_scm_version=True,
        package_dir={"": "src"},
        packages=["syrupy"],
        py_modules=["syrupy"],
        zip_safe=False,
        install_requires=[],
        setup_requires=[],
        entry_points={"pytest11": ["syrupy = syrupy"],},
        python_requires=python_requires,
        classifiers=["Framework :: Pytest"],
    )
