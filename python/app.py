from typing import Optional, Callable

import io_


def app_logic(x: Optional[str], y: Optional[str]) -> str:
    assert isinstance(x, str)
    assert isinstance(y, str)
    return "Result: " + str(int(x) + int(y))


def print_maybe(str_m: Optional[str]) -> io_.IO:
    return io_.put_str_ln(str_m) if str_m is not None else io_._return(None)


def prompt(greet: Optional[str], confirm: Callable[[Optional[str]], str]) -> io_.IO:
    salute = print_maybe(greet)._and(io_.get_line)

    def certify(l: Optional[str]) -> io_.IO:
        return print_maybe(confirm(l))._and(io_._return(l))

    return salute.bind(certify)


def first_number(l: Optional[str]) -> str:
    return "Got first input: " + str(l)


def second_number(l: Optional[str]) -> str:
    return "Got second input: " + str(l)


app = prompt("Please input two numbers.", first_number).bind(
    lambda x: prompt(None, second_number).bind(
        lambda y: io_.put_str_ln(app_logic(x, y))
    )
)

if __name__ == "__main__":
    app.unsafeRunIO()
