from time import sleep
import shlex
from sys import argv

class MOLEBetaException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class MOLEPackageCorrupted(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class MOLEPackageMissing(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class MOLEPackageError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class MOLEInterpreterError(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class nul:
    def __str__(self):
        return "nul"
    def __repr__(self):
        return "nul"

class yea:
    def __str__(self):
        return "yea"
    def __repr__(self):
        return "yea"

class nah:
    def __str__(self):
        return "nah"
    def __repr__(self):
        return "nah"
    
class _BOOL():
    def __init__(self):
        self.yea = yea()
        self.nah = nah()
        self.nul = nul()
_BOOL = _BOOL()

global MOLE

def get_class():
    while "mole" not in globals():
        sleep(0.01)
    return mole

class MOLE:
    def __init__(self) -> None:
        self.variables = {}
        self.random_included = False
        self._ = {"yea": _BOOL.yea, "nah": _BOOL.nah, "nul": _BOOL.nul}

    def warn(self, arg: str):
        print('[Module WARN]', arg.replace("\n", "\n[Module WARN] ")[2:-3])

    def iwarn(self, *args: object):
        print('[Interpreter WARN]', str(args).replace("\n", "\n[Interpreter WARN] ")[2:-3])
    
    def ierror(self, exceptionclass: any, args: str):
        print(f'[Interpreter ERROR from {exceptionclass.__name__}]\n{args.strip("\n")}')
        quit(1)

    def interpret(self, line: list):
        try:
            for ln in line:
                ln = shlex.split(ln) # used "  " as argument here
                #print("[Interpreter line] " + str(ln))
                try:
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
                                        self.variables[ln[1]] = self._["nul"]
                                    elif ln[3] == "yea":
                                        self.variables[ln[1]] = self._["yea"]
                                    elif ln[3] == "nah":
                                        self.variables[ln[1]] = self._["nah"]
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
                            if self.variables[ln[1]] == self._["nul"]:
                                print("nul", end="")
                            elif self.variables[ln[1]] == self._["yea"]:
                                print("yea", end="")
                            elif self.variables[ln[1]] == self._["nah"]:
                                print("nah", end="")
                            else:
                                try:
                                    print(self.variables[ln[1]].replace(r"\n", "\n").replace(r"\r", "\r").replace(r"\"", "\""), end="")
                                except:
                                    print(self.variables[ln[1]], end="")
                        else:
                            if (ln[1][0] == '"' and ln[1][-1] == '"') or (ln[1][0] == "'" and ln[1][-1] == "'"):
                                if ln[1][0] == '"' and ln[1][-1] == '"':
                                    # if not '"' in ln[1][1:-1]:
                                        print(ln[1][1:-1], end="")
                                    # else:
                                        # raise SyntaxError("\" in a double-quoted string")
                                elif ln[1][0] == "'" and ln[1][-1] == "'":
                                    # if not "'" in ln[1][1:-1]:
                                        print(ln[1][1:-1], end="")
                                    # else:
                                    #     raise SyntaxError("' in a single-quoted string")
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
                                #ln[1] = "'" + ln[1] + "'"
                                try:
                                    print(ln[1], end="")
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
                        if ln[1] == "__my_dad__":
                            raise NameError("He went for milk. :P") from None
                        try:
                            with open(ln[1], "r", encoding="utf-8") as included:
                                self.interpret(included.read().splitlines())
                        except FileNotFoundError:
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
                            raise MOLEInterpreterError("The value is NaN")
                    elif ln[0] == "endln":
                        print("")
                    elif ln[0] == "help":
                        print("""
    help for (not) Mighty Old Language Extended:
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
    "randomint [x] [y] [z]": generates a random integer within the range of [x] and [y] to [z]. (requires 'random')
    "eval [in] -> [out]": passes through booleans, turns other values into nul (requires 'statements')
    "if [a] [equals/nequals/lessthan/morethan] [b] -> [c]": an if statement (requires 'statements')
    "[asknumber/askbool/askstr] [x] [STRING]": ask for values
    "execifeval [x] -> [filename]": if a value is `yea`, execute a file or exit if [filename] is "exit"
                        """, end="")
                    elif ln[0] == "use":
                        if ln[1] == "random":
                            try:
                                global randint
                                from __random__ import randint
                            except:
                                self.ierror(MOLEPackageMissing, "")
                        elif ln[1] == "statements":
                            try:
                                global if_statement
                                from __statements__ import if_statement, if_eval, if_file
                            except:
                                self.ierror(MOLEPackageMissing, "")
                        elif ln[1] == "__shell__":
                            try:
                                global Shell
                                from __shell__ import Shell
                            except:
                                self.ierror(MOLEPackageMissing, "")
                        else:
                            raise MOLEPackageMissing
                    elif ln[0] == "randomint":
                        if 'randint' in globals():
                            self.variables[ln[3]] = (randint(int(ln[1]), int(ln[2])))
                        else:
                            # while 'randint' not in globals():
                            #     sleep(0.01)
                            self.ierror(MOLEPackageCorrupted, "")
                        #("'randomint' is not a valid keyword. did you forget to use 'random'?")
                    elif ln[0] == "warn":
                        try:
                            self.warn(ln[1].strip())
                        except IndexError:
                            self.iwarn("received a warning request with no message, ignoring")
                    elif ln[0] == "__shell__":
                        self.iwarn("Shell() is permanent until removed from the file and MOLE is restarted.")
                        try:
                            shell = Shell() #self.variables)
                        except NameError:
                            raise MOLEPackageMissing("Cannot initialize Shell, did you forget to `use __shell__`?")
                        except:
                            raise MOLEPackageCorrupted from RuntimeError("Failure to run the package")
                    elif ln[0] == "askbool":
                        if ln[1].strip() == "":
                            raise SyntaxError("you need to pass a variable in the first argument, otherwise the expression would be pointless")
                        else:
                            input_value = input((ln[2]) + " [y/n] ")
                            if input_value == "y" or input_value == "yes":
                                self.variables[ln[1]] = self._["yea"]
                            elif input_value == "n" or input_value == "no":
                                self.variables[ln[1]] = self._["nah"]
                            else:
                                self.variables[ln[1]] = self._["nul"]
                    elif ln[0] == "if":
                        try:
                            if len(ln) == 6 and ln[4] == "->":
                                if ln[1] in self.variables and ln[3] in self.variables:
                                    try:
                                        self.variables[ln[5]] = if_statement(self.variables[ln[1]], self.variables[ln[3]], ln[2], self._["yea"], self._["nah"], self._["nul"])
                                    except NameError:
                                        raise MOLEPackageMissing("Cannot execute if operation, did you forget to `use statements`?")
                                else:
                                    raise SyntaxError("Not a valid variable") #("I don't know what is wrong, DM the developer of this or something")
                            else:
                                raise SyntaxError("Malformed if syntax")
                                # self.variables[ln[4]] = if_statement(self.variables[ln[1]], ln[2]) if ln[3] == "saveto" else self._["nul"]
                        except Exception as e:
                            raise MOLEPackageError("An error occured inside the MOLE interpreter or one of the used packages")
                    elif ln[0] == "eval":
                        if len(ln) == 4 and ln[1] in self.variables and ln[2] == "->":
                            try:
                                self.variables[ln[3]] = if_eval(self.variables[ln[1]], self._["yea"], self._["nah"], self._["nul"])
                            except:
                                raise MOLEInterpreterError from MOLEPackageError
                    elif ln[0] == "exit":
                        return
                    elif ln[0] == "asknumber":
                        try:
                            input_value = float(input((ln[2])))
                            self.variables[ln[1]] = input_value
                        except IndexError:
                            raise MOLEInterpreterError("Could not get the value") from SyntaxError(NotImplemented)
                        except ValueError:
                            raise MOLEInterpreterError("Invalid value") from ValueError("Invalid value")
                    elif ln[0] == "askstr":
                        try:
                            self.variables[ln[1]] = input(ln[2])
                        except KeyboardInterrupt:
                            raise MOLEInterpreterError("Pressed ^C")
                    elif ln[0] == "execifeval":
                        try:
                            if if_file(self.variables[ln[1]], self._["yea"], self._["nah"]) == self._["yea"]:
                                if ln[2] != "exit":
                                    with open(ln[2] + ".mole", "r", encoding="utf-8") as included:
                                        self.interpret(included.read().splitlines())
                                else:
                                    exit()
                        except FileNotFoundError:
                            raise RuntimeError(f"execution failed; no such file {ln[2]}")
                        except NameError:
                            raise MOLEInterpreterError("You have to `use statements` in your code to use if statements.")
                    else:
                        raise SyntaxError(f"{ln[0]} is not a valid keyword")
                except IndexError:
                    pass
        except Exception as e:
            raise e

mole = MOLE()

version = "v2.4.1"
version_name = "Feature Update 2 Subrelease 4 Patch 1"
if __name__ == "__main__" and not "--nologo" in argv:
    print(f"MOLE version {version} ({version_name}) - made by orca.pet")
    if version[-1] == "b":
        mole.iwarn(f"beta version ahead; use at your own risk")

if __name__ == "__main__":
    maincode = open(argv[1], "r+", encoding="utf-8").read().splitlines()
    mole.interpret(maincode)
    if "--pause-on-exit" in argv or "-p" in argv:
        input("Press enter to exit or drop to shell (-s).")
    if "-s" in argv:
        mole.interpret(["use __shell__", "__shell__"])

# self._["yea"], self._["nah"], self._["nul"]


