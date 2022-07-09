class Queue:
    def __init__(self):
        self._variables = []

    def pop(self):
        var_to_return = self._variables[0]
        self._variables = self._variables[1:]
        return var_to_return

    def push(self, var):
        self._variables.append(var)

    def len(self):
        return len(self._variables)
