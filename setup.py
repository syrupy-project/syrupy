import sys
from datetime import datetime

from setuptools import (
    find_packages,
    setup,
)


python_requires = "~=3.6"
setup_requires = ["setuptools_scm"]
install_requires = ["attrs>=18.2.0", "colored", "typing_extensions>=3.6"]
dev_requires = [
    "black",
    "codecov",
    "coverage[toml]",
    "flake8",
    "flake8-bugbear",
    "flake8-builtins",
    "flake8-comprehensions",
    "flake8-i18n",
    "invoke",
    "isort",
    "mypy",
    "pip-tools",
    "py-githooks",
    "pytest",
    "semver",
    "twine",
    "wheel",
]

if sys.version_info[0] == 2:
    raise Exception("Only python 3 supported.")


def readme() -> str:
    with open("README.md") as f:
        return f.read()


if __name__ in ["__main__", "builtins"]:
    setup(
        name="syrupy",
        description="PyTest Snapshot Test Utility",
        author="Top Hat Open Source",
        author_email="opensource@tophat.com",
        license="Apache License 2.0",
        url="https://github.com/tophat/syrupy",
        long_description=readme(),
        long_description_content_type="text/markdown",
        use_scm_version={
            "local_scheme": lambda _: "",
            "version_scheme": lambda v: v.format_with("{tag}")
            if v.exact
            else datetime.now().strftime("%Y.%m.%d.%H%M%S%f"),
            "write_to": "version.txt",
        },
        package_dir={"": "src"},
        packages=find_packages("./src"),
        zip_safe=False,
        entry_points={"pytest11": ["syrupy = syrupy"]},
        extras_require={"dev": dev_requires},
        install_requires=install_requires,
        setup_requires=setup_requires,
        python_requires=python_requires,
        classifiers=[
            "Development Status :: 1 - Planning",
            "Framework :: Pytest",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries",
        ],
    )
