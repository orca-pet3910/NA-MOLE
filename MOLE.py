from time import sleep
import shlex
from io import BytesIO

version = "v2.0"
print(f"MOLE version {version} - made by orca.pet")

maincode = open(__import__("sys").argv[1], "r+", encoding="utf-8").read().splitlines()
for line in maincode:
    line.split("  ")

class MOLEBetaException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class nul:
    def __str__(self):
        return "nul"
    def __repr__(self):
        return "nul"
nul = nul()

class yea:
    def __str__(self):
        return "yea"
    def __repr__(self):
        return "yea"
yea = yea()

class nah:
    def __str__(self):
        return "nah"
    def __repr__(self):
        return "nah"
nah = nah()

global MOLE

class MOLE:
    def __init__(self) -> None:
        self.variables = {}
        self.random_included = False

    def warn(self, arg: str):
        print('[Module WARN]', arg.replace("\n", "\n[Module WARN] ")[2:-3])

    def iwarn(self, *args: object):
        print('[Interpreter WARN]', str(args).replace("\n", "\n[Interpreter WARN] ")[2:-3])
    
    def ierror(self, exceptionclass: any, args: str):
        print(f'[Interpreter ERROR from {exceptionclass.__name__}] {args}')
        quit(1)

    def interpret(self, line: list):
            try:
                for ln in line:
                    ln = shlex.split(ln) # used "  " as argument here
                    #print("[Interpreter line] " + str(ln))
                    if ln[0] == "let":
                        if ln[2] == "be":
                            raise_ = False
                            if ln[3] in self.variables:
                                self.variables[ln[1]] = self.variables[ln[3]]
                            else:
                                try:
                                    self.variables[ln[1]] = float(ln[3])
                                except ValueError:
                                    if ln[3] == "nul":
                                        self.variables[ln[1]] = nul
                                    elif ln[3] == "yea":
                                        self.variables[ln[1]] = yea
                                    elif ln[3] == "nah":
                                        self.variables[ln[1]] = nah
                                    else:
                                        self.variables[ln[1]] = ln[3].replace(r"\n", "\n")
                                    # else:
                                    #     raise_ = True
                                if raise_:
                                    raise NameError(f"{ln[3]} is not a valid value")
                        else:
                            raise SyntaxError("missing 'be' statement in variable definition ('=' is 'be' in this language, cuz why not)")

                    elif ln[0] == "print":
                        if ln[1] in self.variables:
                            if self.variables[ln[1]] == nul:
                                print("[Module] nul", end="")
                            elif self.variables[ln[1]] == yea:
                                print("[Module] yea", end="")
                            elif self.variables[ln[1]] == nah:
                                print("[Module] nah", end="")
                            else:
                                try:
                                    print("[Module]", self.variables[ln[1]].replace(r"\n", "\n").replace(r"\r", "\r").replace(r"\"", "\"").replace("\n", "\n[Module] "), end="")
                                except:
                                    print("[Module]", self.variables[ln[1]], end="")
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
                                print("[Module] nul", end="")
                            elif ln[1] == "yea":
                                print("[Module] yea", end="")
                            elif ln[1] == "nah":
                                print("[Module] nah", end="")
                            else:
                                #ln[1] = "'" + ln[1] + "'"
                                try:
                                    print("[Module]", ln[1], end="")
                                except:
                                    raise NameError(f"{ln[1]} is not a valid value") from None
                    elif ln[0].startswith("-!-"):
                        pass
                    elif ln[0] == "getallvar":
                        print(self.variables, end="")
                    elif ln[0] == "add":
                        try:
                            self.variables[ln[1]] += float(ln[2])
                        except KeyError:
                            raise ValueError(f"there is no such variable called '{ln[1]}'") from None
                    elif ln[0] == "sub":
                        try:
                            self.variables[ln[1]] -= float(ln[2])
                        except KeyError:
                            raise ValueError(f"there is no such variable called '{ln[1]}'") from None
                    elif ln[0] == "mul":
                        try:
                            self.variables[ln[1]] *= float(ln[2])
                        except KeyError:
                            raise ValueError(f"there is no such variable called '{ln[1]}'") from None
                    elif ln[0] == "div":
                        db0raise = False
                        try:
                            self.variables[ln[1]] /= float(ln[2])
                        except KeyError:
                            raise ValueError(f"there is no such variable called '{ln[1]}'") from None
                        except ZeroDivisionError:
                            db0raise = True
                        if db0raise:
                            raise ZeroDivisionError(f"an attempt was made to divide {self.variables[ln[1]]} by zero - don't do that at home kids ;)")
                    elif ln[0] == "include":
                        execute_failed = False
                        if ln[1] == "__my_dad__":
                            raise NameError("He went for milk. :P") from None
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
    help:
    "afk [seconds]": wait for [seconds] seconds
    "endln": prints a line break
    "eat [variable]": deletes [variable] from the universe
    "include [scriptname]": reads content of [scriptname] and attempts to execute it
    "[add/sub/mul/div] [variablename] [number]": performs a math operation on [variablename]
    "getallvar": prints out a Python-formatted dictionary of variables (this is how variables are stored)
    "-!- [message]": a no-operation instruction. "-!-", as well as text after it, will be ignored, making it good for commenting
    "print [variablename/(number/bool/nul/string value)]": prints that to the console
    "let variablename be [string/nul/bool/number value]": variable definition. defines variablename and its value, [string/nul/bool/number value] (in
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
                    elif ln[0] == "__shell__":
                        self.iwarn("Shell() is permanent until removed from the file and MOLE is restarted.")
                        shell = Shell()
                    elif ln[0] == "askbool":
                        if ln[1].strip() == "":
                            raise SyntaxError("you need to pass a variable in the first argument, otherwise the expression would be pointless")
                        else:
                            input_value = input("\n" + ln[2] + " [y/n] ")
                            if input_value == "y" or input_value == "yes":
                                self.variables[ln[1]] = yea
                            elif input_value == "n" or input_value == "no":
                                self.variables[ln[1]] = nah
                            else:
                                self.variables[ln[1]] = nul
                    else:
                        raise SyntaxError(f"{ln[0]} is not a valid keyword")
            except Exception as e:
                try:
                    self.ierror(e.__class__, str(e.args[0]))
                except:
                    self.ierror(e.__class__, "\b")

class Shell(MOLE):
    def __init__(self):
        shell = MOLE()
        while True:
            command = input("\n>>> ")
            shell.interpret(line=[command])


mole = MOLE()
if version[-1] == "b":
    mole.iwarn(f"beta version ahead; use at your own risk")

mole.interpret(maincode)
