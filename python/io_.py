from typing import Callable, Optional, TypeVar, Generic

T = TypeVar("T")


class IO(Generic[T]):
    def __init__(self, run: Callable[[], Optional[T]]) -> None:
        self.unsafeRunIO = run

    def map(self, f: Callable[[Optional[T]], Optional[T]]) -> "IO[T]":
        return IO(lambda: f(self.unsafeRunIO()))

    def bind(self, f: Callable[[Optional[T]], "IO[T]"]) -> "IO[T]":
        return IO(lambda: f(self.unsafeRunIO()).unsafeRunIO())

    def _and(self, other: "IO[T]") -> "IO[T]":
        def go() -> Optional[T]:
            self.unsafeRunIO()
            return other.unsafeRunIO()

        return IO(go)


def _return(x: Optional[T]) -> IO[T]:
    return IO(lambda: x)


def put_str_ln(s: T) -> IO[T]:
    def go() -> None:
        print(s)
        return None

    return IO(go)


get_line = IO(input)
