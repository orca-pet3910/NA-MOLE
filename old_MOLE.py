from time import sleep

version = "v1.1b"

maincode = open("./main.ol", "r+", encoding="utf-8").read().splitlines()
for line in maincode:
    line.split("  ")

class ModuleEmptyError(BaseException):
    def __init__(self, *args: object) -> None:
        print("[Module ERROR] found no contents, raising exception")
        super().__init__(*args)

class OlBetaException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

global Ol

class Ol:
    def __init__(self) -> None:
        self.variables = {}
        self.random_included = False

    def warn(self, arg: str):
        print('[Module WARN] ', arg.replace("\n", "\n[Module WARN] "))

    def iwarn(self, *args: object):
        print('[Interpreter WARN] ', str(args).replace("\n", "\n[Interpreter WARN] "))

    def interpret(self, line: list):
            for ln in line:
                ln = ln.split("  ")
                if ln[0] == "let":
                            if ln[2] == "be":
                                raise_ = False
                                if ln[3] in self.variables:
                                    self.variables[ln[1]] = self.variables[ln[3]]
                                else:
                                    try:
                                        self.variables[ln[1]] = float(ln[3])
                                    except ValueError:
                                        if (ln[3][0] == '"' and ln[3][-1] == '"') or (ln[1][0] == "'" and ln[3][-1] == "'") or (ln[3] == "nul") or (ln[3] == "yea") or (ln[3] == "nah"):
                                            if ln[3] == "nul":
                                                self.variables[ln[1]] = None
                                            elif ln[3] == "yea":
                                                self.variables[ln[1]] = True
                                            elif ln[3] == "nah":
                                                self.variables[ln[1]] = False
                                            else:
                                                self.variables[ln[1]] = ln[3][1:-1].replace(r"\n", "\n")
                                        else:
                                            raise_ = True
                                    if raise_:
                                        raise NameError(f"{ln[3]} is not a valid value")
                            else:
                                raise SyntaxError("missing 'be' statement in variable definition ('=' is 'be' in this language, cuz why not)")

                elif ln[0] == "print":
                    if ln[1] in self.variables:
                        if self.variables[ln[1]] == None:
                            print("nul", end="")
                        elif self.variables[ln[1]] == True:
                            print("yea", end="")
                        elif self.variables[ln[1]] == False:
                            print("nah", end="")
                        else:
                            try:
                                print(self.variables[ln[1]].replace(r"\b", "\b").replace(r"\n", "\n").replace(r"\r", "\r").replace(r"\"", "\""))
                            except:
                                print(self.variables[ln[1]])
                    else:
                        if (ln[1][0] == '"' and ln[1][-1] == '"') or (ln[1][0] == "'" and ln[1][-1] == "'"):
                            if ln[1][0] == '"' and ln[1][-1] == '"':
                                if not '"' in ln[1][1:-1]:
                                    print(ln[1][1:-1], end="")
                                else:
                                    raise SyntaxError("\" in a double-quoted string")
                            elif ln[1][0] == "'" and ln[1][-1] == "'":
                                if not "'" in ln[1][1:-1]:
                                    print(ln[1][1:-1], end="")
                                else:
                                    raise SyntaxError("' in a single-quoted string")
                            # else:
                            #     try:
                            #         print(float(ln[1]))
                            #     except:
                            #         raise Exception("an error occured, please contact the developer")
                        elif ln[1] == "nul":
                            print("nul", end="")
                        elif ln[1] == "yea":
                            print("yea", end="")
                        elif ln[1] == "nah":
                            print("nah", end="")
                        else:
                            try:
                                print(float(ln[1]))
                            except:
                                raise NameError(f"{ln[1]} is not a valid variable") from None
                elif ln[0].startswith("-!-"):
                    pass
                elif ln[0] == "getallvar":
                    print(self.variables, end="")
                elif ln[0] == "add":
                    try:
                        self.variables[ln[1]] += float(ln[2])
                    except KeyError:
                        raise ValueError(f"there is no such variable called '{ln[1]}'")
                elif ln[0] == "sub":
                    try:
                        self.variables[ln[1]] -= float(ln[2])
                    except KeyError:
                        raise ValueError(f"there is no such variable called '{ln[1]}'")
                elif ln[0] == "mul":
                    try:
                        self.variables[ln[1]] *= float(ln[2])
                    except KeyError:
                        raise ValueError(f"there is no such variable called '{ln[1]}'")
                elif ln[0] == "div":
                    db0raise = False
                    try:
                        self.variables[ln[1]] /= float(ln[2])
                    except KeyError:
                        raise ValueError(f"there is no such variable called '{ln[1]}'")
                    except ZeroDivisionError:
                        db0raise = True
                    if db0raise:
                        raise ZeroDivisionError(f"an attempt was made to divide {self.variables[ln[1]]} by zero - don't do that at home kids ;)")
                elif ln[0] == "include":
                    execute_failed = False
                    try:
                        with open(ln[1], "r", encoding="utf-8") as included:
                            self.interpret(included.read().splitlines())
                    except FileNotFoundError:
                        execute_failed = True
                    if execute_failed:
                        raise RuntimeError(f"execution failed; no such file {ln[1]}")
                elif ln[0] == "eat":
                    fail = False
                    try:
                        del self.variables[ln[1]]
                    except KeyError:
                        fail = True
                    if fail:
                        raise NameError(f"cannot eat {ln[1]}; this variable does not exist")
                elif ln[0] == "afk":
                    try:
                        if ln[1] in self.variables:
                            sleep(self.variables[ln[1]])
                        else:
                            sleep(float(ln[1]))
                    except ValueError:
                        raise Exception("whoops")
                elif ln[0] == "endln":
                    print("")
                elif ln[0] == "help":
                    print("""
help (SEPARATE ARGUMENTS AND STATEMENTS WITH DOUBLE SPACES!!!):
"afk  [seconds]": wait for [seconds] seconds
"endln": prints a line break
"eat  [variable]": deletes [variable] from the universe
"include [scriptname]": reads content of [scriptname] and attempts to execute it
"[add/sub/mul/div]  [variablename]  [number]": performs a math operation on [variablename]
"getallvar": prints out a Python-formatted dictionary of variables (this is how variables are stored)
"-!-  [message]": a no-operation instruction. "-!-", as well as text after it, will be ignored
"print  [variablename/(number/bool/nul/string value)]": prints that to the console
"let  variablename  be  [string/nul/bool/number value]": variable definition. defines variablename and its value, [string/nul/bool/number value] (in
other words: adds the variable to the variables dictionary)
"use [object]": includes an object, for example "random" will unlock "randomint [x] [y]"
"randomint [x] [y]": generates a random integer within the range of [x] and [y]. (requires 'random')
                    """, end="")
                elif ln[0] == "use":
                    if ln[1] == "random":
                        import random
                        self.random_included = True
                elif ln[0] == "randomint":
                    if self.random_included:
                        print(random.randint(int(ln[1]), int(ln[2])), end="")
                    else:
                        raise NameError("'randomint' is not a valid keyword. did you forget to use 'random'?")
                elif ln[0] == "warn":
                    try:
                        self.warn(ln[1].strip())
                    except IndexError:
                        self.iwarn("received a warning request with no message, ignoring")
                elif ln[0].strip() == "":
                    pass
                else:
                    raise SyntaxError(f"{ln[0]} is not a valid keyword")

class Shell(Ol):
    def __init__(self):
        shell = Ol()
        while True:
            command = input("\n>>> ")
            shell.interpret(line=[command])


ol = Ol()
ol.iwarn("this project is WIP, expect bugs with new features")
if version[-1] == "b":
    ol.iwarn(f"beta version ahead ({version}); use at your own risk")
ol.interpret(maincode)