from typing import Optional, Callable

import io_


def app_logic(x: str, y: str) -> str:
    return "Result: " + str(int(x) + int(y))


def print_maybe(str_m: Optional[str]) -> io_.IO[None]:
    return io_.put_str_ln(str_m) if str_m is not None else io_._return(None)


def prompt(greet: Optional[str], confirm: Callable[[str], str]) -> io_.IO[str]:
    salute = print_maybe(greet)._and(io_.get_line)

    def certify(l: str) -> io_.IO[str]:
        return print_maybe(confirm(l))._and(io_._return(l))

    return salute.bind(certify)


def first_number(l: str) -> str:
    return "Got first input: " + str(l)


def second_number(l: str) -> str:
    return "Got second input: " + str(l)


def input_second_number_and_print_result(x: str) -> io_.IO[None]:
    def print_result(y: str) -> io_.IO[None]:
        return io_.put_str_ln(app_logic(x, y))

    return prompt(None, second_number).bind(print_result)


app = prompt("Please input two numbers.", first_number).bind(
    input_second_number_and_print_result
)

if __name__ == "__main__":
    app.unsafeRunIO()
