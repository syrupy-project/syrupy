import os
import sys

from setuptools import setup

python_requires = "~=3.6"

test_requires = [
    "pytest",
    "black",
    "invoke",
    "pyyaml",
    "mypy"
]

if sys.version_info[0] == 2:
    raise Exception("Only python 3 supported.")

if __name__ == "__main__":
    setup(
        name="th_snapshot",
        description="Top Hat Snapshot Test Utility",
        author="Top Hat Open Source",
        use_scm_version=True,
        package_dir={"": "src"},
        packages=["th_snapshot"],
        py_modules=["th_snapshot"],
        zip_safe=False,
        install_requires=[],
        setup_requires=[],
        extras_require={
            "test": test_requires,
        },
        entry_points={
            "pytest11": ["th_snapshot = th_snapshot"],
        },
        python_requires=python_requires,
        classifiers=["Framework :: Pytest"]
    )
