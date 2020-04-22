from typing import Any, Callable, TypeVar

ReturnType = TypeVar("ReturnType")

def fixture(func: Callable[..., ReturnType]) -> Callable[..., ReturnType]: ...
