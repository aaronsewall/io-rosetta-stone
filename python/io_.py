from typing import Callable, TypeVar, Generic

T = TypeVar("T")
S = TypeVar("S")


class IO(Generic[T]):
    def __init__(self: "IO[T]", run: Callable[..., T]) -> None:
        self.unsafeRunIO = run

    def map(self: "IO[T]", f: Callable[..., T]) -> "IO[T]":
        return IO(lambda: f(self.unsafeRunIO()))

    def bind(self: "IO[T]", f: Callable[..., "IO[S]"]) -> "IO[S]":
        return IO(lambda: f(self.unsafeRunIO()).unsafeRunIO())

    def _and(self: "IO[T]", other: "IO[S]") -> "IO[S]":
        def go() -> S:
            self.unsafeRunIO()
            return other.unsafeRunIO()

        return IO(go)


def _return(x: T) -> IO[T]:
    return IO(lambda: x)


def put_str_ln(s: str) -> IO[None]:
    def go() -> None:
        print(s)

    return IO(go)


get_line = IO(input)
