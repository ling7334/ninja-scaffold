from typing import Any, Callable, Dict, TypeVar, Union

TResponse = TypeVar("TResponse", bound=Callable[..., Any])

TStatusResponse = TypeVar("TStatusResponse", bound=Callable[..., Union[int, Any]])

TResponses = Union[TResponse, TStatusResponse]
