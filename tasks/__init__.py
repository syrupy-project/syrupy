from invoke import Collection

from . import (
    benchmark,
    build,
    lint,
    test,
)

ns = Collection()
# Top level tasks
ns.add_task(benchmark.benchmark)
ns.add_task(build.install)
ns.add_task(test.test)
# Module collection tasks
ns.add_collection(lint)
