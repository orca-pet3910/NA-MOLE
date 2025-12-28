def read(filename: str) -> str:
    cont = open(filename, "r", encoding="utf-8").read()
    return cont