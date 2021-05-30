import os
import re

from invoke import task

from setup import install_requires

from .utils import ctx_run


def _parse_min_versions(requirements):
    result = []
    for req in sorted(requirements):
        match = re.match(r"([\w_]+)>=([^,]+),.*", req)
        if match is None:
            continue
        pkg_name = match.group(1)
        min_version = match.group(2)
        result.append(f"{pkg_name}=={min_version}")
    return result


@task
def requirements(ctx, upgrade=False):
    """
    Build test & dev requirements lock file
    """
    args = [
        "--no-emit-find-links",
        "--no-emit-index-url",
        "--allow-unsafe",
        "--rebuild",
    ]
    if upgrade:
        args.append("--upgrade")
    ctx_run(
        ctx,
        f"echo '-e .[dev]' | python -m piptools compile "
        f"{' '.join(args)} - -qo- | sed '/^-e / d' > dev_requirements.txt",
    )

    with open("min_requirements.constraints", "w", encoding="utf-8") as f:
        min_requirements = _parse_min_versions(install_requires)
        f.write("\n".join(min_requirements))
        f.write("\n")


@task
def clean(ctx):
    """
    Remove build files e.g. package, distributable, compiled etc.
    """
    ctx_run(ctx, "rm -rf *.egg-info dist build __pycache__ .pytest_cache artifacts/*")


@task(pre=[clean])
def dist(ctx):
    """
    Generate version from scm and build package distributable
    """
    ctx_run(ctx, "python setup.py sdist bdist_wheel")


@task
def publish(ctx, dry_run=True):
    """
    Upload built package to pypi
    """
    repo_url = "--repository-url https://test.pypi.org/legacy/" if dry_run else ""
    ctx_run(ctx, f"twine upload --skip-existing {repo_url} dist/*")


@task(pre=[dist])
def release(ctx, dry_run=True):
    """
    Build and publish package to pypi index based on scm version
    """
    from semver import parse_version_info

    if not dry_run and not os.environ.get("CI"):
        print("This is a CI only command")
        exit(1)

    # get version created in build
    with open("version.txt", "r", encoding="utf-8") as f:
        version = str(f.read())

    try:
        should_publish_to_pypi = not dry_run and parse_version_info(version)
    except ValueError:
        should_publish_to_pypi = False

    # publish to test to verify builds
    if dry_run:
        publish(ctx, dry_run=True)

    # publish to pypi if test succeeds
    if should_publish_to_pypi:
        publish(ctx, dry_run=False)
