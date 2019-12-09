from collections import namedtuple


TestLocation = namedtuple(
    "TestLocation",
    ["filename", "modulename", "classname", "methodname", "nodename", "testname"],
)
