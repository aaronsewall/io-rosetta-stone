from typing import Callable, Optional


class IO:
    def __init__(self: "IO", run: Callable[[], Optional[str]]) -> None:
        self.unsafeRunIO = run

    def map(self: "IO", f: Callable[[Optional[str]], Optional[str]]) -> "IO":
        return IO(lambda: f(self.unsafeRunIO()))

    def bind(self: "IO", f: Callable[[Optional[str]], "IO"]) -> "IO":
        return IO(lambda: f(self.unsafeRunIO()).unsafeRunIO())

    def _and(self: "IO", other: "IO") -> "IO":
        def go() -> Optional[str]:
            self.unsafeRunIO()
            return other.unsafeRunIO()

        return IO(go)


def _return(x: Optional[str]) -> IO:
    return IO(lambda: x)


def put_str_ln(s: str) -> IO:
    def go() -> None:
        print(s)
        return None

    return IO(go)


get_line = IO(input)
