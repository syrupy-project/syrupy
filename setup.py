import sys
from datetime import datetime

from setuptools import (
    find_packages,
    setup,
)


PYTHON_REQUIRES = "~=3.6"

if sys.version_info[0] == 2:
    raise Exception("Only python 3 supported.")


def readme() -> str:
    with open("README.md") as f:
        return f.read()


def local_scheme(v) -> str:
    return ""


def version_scheme(v) -> str:
    return (
        v.format_with("{tag}")
        if v.exact
        else datetime.now().strftime("%Y.%m.%d.%H%M%S%f")
    )


if __name__ == "__main__":
    setup(
        name="syrupy",
        description="PyTest Snapshot Test Utility",
        author="Top Hat Open Source",
        author_email="opensource@tophat.com",
        url="https://github.com/tophat/syrupy",
        long_description=readme(),
        long_description_content_type="text/markdown",
        use_scm_version={
            "local_scheme": local_scheme,
            "version_scheme": version_scheme,
            "write_to": "version.txt",
        },
        package_dir={"": "src"},
        packages=find_packages("./src"),
        zip_safe=False,
        install_requires=["pyyaml"],
        setup_requires=["setuptools_scm"],
        entry_points={"pytest11": ["syrupy = syrupy"]},
        python_requires=PYTHON_REQUIRES,
        classifiers=[
            "Development Status :: 1 - Planning",
            "Framework :: Pytest",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries",
        ],
    )
