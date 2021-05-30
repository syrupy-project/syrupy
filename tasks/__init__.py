from invoke import Collection

from . import (
    benchmark,
    build,
    install,
    lint,
    test,
)

ns = Collection()
# Top level tasks
ns.add_task(benchmark.benchmark)
ns.add_task(build.dist, name="build")
ns.add_task(build.requirements)
ns.add_task(build.release)
ns.add_task(test.test)
# Module collection tasks
ns.add_collection(install)
ns.add_collection(lint)
