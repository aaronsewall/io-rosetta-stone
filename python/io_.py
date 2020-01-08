from typing import Callable, Optional, TypeVar

T = TypeVar("T")


class IO:
    def __init__(self: "IO", run: Callable[[], Optional[T]]) -> None:
        self.unsafeRunIO = run

    def map(self: "IO", f: Callable[[Optional[T]], Optional[T]]) -> "IO":
        return IO(lambda: f(self.unsafeRunIO()))

    def bind(self: "IO", f: Callable[[Optional[T]], "IO"]) -> "IO":
        return IO(lambda: f(self.unsafeRunIO()).unsafeRunIO())

    def _and(self: "IO", other: "IO") -> "IO":
        def go() -> Optional[T]:
            self.unsafeRunIO()
            return other.unsafeRunIO()

        return IO(go)


def _return(x: Optional[T]) -> IO:
    return IO(lambda: x)


def put_str_ln(s: T) -> IO:
    def go() -> None:
        print(s)
        return None

    return IO(go)


get_line = IO(input)
