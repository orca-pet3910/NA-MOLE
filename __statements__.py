from MOLE import sleep, MOLEPackageError
# MOLE = get_class()
# yea, nah, nul = MOLE._["yea"], MOLE._["nah"], MOLE._["nul"]
sleep(0.01)
def if_statement(value1, value2, operation: str, yea, nah, nul):
    # print(type(value1))
    # print(type(value2))
    try:
        if operation == "equals":
            if value1 == value2:
                return yea
            else:
                return nah
        elif operation == "nequals":
            if value1 != value2:
                return yea
            else:
                return nah
        elif operation == "lessthan":
            if value1 < value2:
                return yea
            else:
                return nah
        elif operation == "morethan":
            if value1 > value2:
                return yea
            else:
                return nah
        else:
            raise MOLEPackageError("Undefined operation")
    except MOLEPackageError:
        raise
    except TypeError:
        raise MOLEPackageError("Trying to compare incomparable types")
    
def if_eval(value1, yea, nah, nul):
    # print(type(value1))
    # print(type(yea))
    # print(type(nah))
    # print(type(nul))
    if value1 is yea:
        # print("yes")
        return yea
    elif value1 is nah:
        # print("no")
        return nah
    else:
        # print("neither")
        return nul
    
def if_file(value1, yea, nah):
    if value1 == yea:
        return yea
    else:
        return nah