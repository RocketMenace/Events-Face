from secrets import randbelow


def generate_code() -> str:
    code = randbelow(10000)
    return f"{code:04d}"
