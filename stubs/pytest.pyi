from typing import TypeVar, Callable, Any

ReturnType = TypeVar("ReturnType")

def fixture(func: Callable[..., ReturnType]) -> Callable[..., ReturnType]: ...
