import sys
from datetime import datetime

from setuptools import (
    find_packages,
    setup,
)


python_requires = ">=3.6"
setup_requires = ["setuptools_scm"]
install_requires = [
    "attrs>=18.2.0,<20.0.0",
    "colored>=1.3.92,<2.0.0",
    "typing_extensions>=3.6,<4.0.0",
    "pytest>=5.1.0,<6.0.0",
]
test_requires = [
    "codecov",
    "coverage[toml]",
    "invoke",
]
dev_requires = [
    "black",
    "flake8-bugbear",
    "flake8-builtins",
    "flake8-comprehensions",
    "flake8-i18n",
    "flake8",
    "isort",
    "mypy",
    "pip-tools",
    "py-githooks",
    "pygithub",
    "pyperf",
    "semver",
    "twine",
    "wheel",
    *test_requires,
]

if sys.version_info < (3, 6):
    raise RuntimeError("Only Python 3.6+ supported.")


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
            "Development Status :: 4 - Beta",
            "Framework :: Pytest",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries",
        ],
    )
