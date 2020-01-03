import sys
from datetime import datetime

from setuptools import (
    find_packages,
    setup,
)


python_requires = "~=3.6"
setup_requires = ["setuptools_scm"]
install_requires = ["typing_extensions>=3.6"]
dev_requires = [
    "black==19.10b0",
    "codecov==2.0.15",
    "coverage[toml]==5.0.1",
    "flake8==3.7.9",
    "flake8-bugbear==19.8.0",
    "flake8-builtins==1.4.2",
    "flake8-comprehensions==3.1.4",
    "flake8-i18n==0.1.0",
    "invoke==1.3.0",
    "isort==4.3.21",
    "mypy==0.761",
    "pip-tools==4.3.0",
    "py-githooks==1.1.0",
    "pytest==5.3.2",
    "semver==2.9.0",
    "twine==3.1.1",
    "wheel==0.33.6",
]

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
