from MOLE import get_class

global mole
mole = get_class()

class Shell:
    def __init__(self, variables: dict | None = {}):
        shell = mole
        self.variables = variables
        shell.variables = self.variables
        while True:
            try:
                command = input("\nMOLE>> ")
                if command == "exit": exit()
                shell.interpret(line=[command])
            except Exception as e:
                raise e #mole.iwarn(str(e.__class__.args))
                continue