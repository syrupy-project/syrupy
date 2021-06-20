import sys
from datetime import datetime

from setuptools import (
    find_packages,
    setup,
)

python_requires = ">=3.6"
setup_requires = ["setuptools_scm"]
install_requires = [
    "attrs>=18.2.0,<22.0.0",
    "colored>=1.3.92,<2.0.0",
    "pytest>=5.1.0,<7.0.0",
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
    with open("README.md", encoding="utf-8") as f:
        return f.read()


def version_scheme(v):
    if v.exact:
        return v.format_with("{tag}")
    return datetime.now().strftime("%Y.%m.%d.%H%M%S%f")


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
            "version_scheme": version_scheme,
            "write_to": "version.txt",
        },
        package_dir={"": "src"},
        package_data={"": ["py.typed"]},
        packages=find_packages("./src"),
        zip_safe=False,
        entry_points={"pytest11": ["syrupy = syrupy"]},
        extras_require={"dev": dev_requires, "test": test_requires},
        install_requires=install_requires,
        setup_requires=setup_requires,
        python_requires=python_requires,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Framework :: Pytest",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Testing",
        ],
    )
