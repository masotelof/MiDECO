import numpy as np
import logging as log
import json, time


class Parameters:
    def __init__(self, param=None):
        self.parameter = {'Population': 0,
                          'Function_Calls': 0,
                          'Dimension': 0,
                          'Runs': 0,
                          'LB': 0.0,
                          'UB': 0.0}

        if isinstance(param, dict):
            self.parameter.update(param)

    def __str__(self):
        return json.dumps(self.parameter, indent=4)


class Function:
    def eval(self, items):
        pass


class FunctionCalls:
    def __init__(self, maxValue):
        self.max = maxValue
        self.current = 0

    def isAvailable(self):
        if self.current < self.max:
            return True
        else:
            return False

    def addFunctionCall(self):
        self.current += 1
        if self.current > self.max:
            raise FunctionCallException


class FunctionCallException(Exception):
    def __init__(self, message="It was exceeded the Function Calls"):
        super().__init__(message)


class binary(int):
    __module__ = None


class Metaheuristic():
    parameters = None

    def __init__(self, parameter, function, dtype=binary, name=None):
        self.parameters = parameter
        self.function = function
        self.dtype = dtype
        self.items = []
        self.name = name
        self.functionCall = FunctionCalls(self.parameters.parameter['Function_Calls'])


class Item:
    parameters = None

    def __init__(self, parameter, function, dtype=binary, values=None):
        self.parameters = parameter
        self.function = function
        self.dtype = dtype
        self.fitness = 0
        if values is None:
            self.values = np.array([])
        else:
            self.values = values[:]

    def initialization(self):
        try:
            if self.dtype is int:
                self.values = np.random.random_integers(self.parameters.parameter['LB'], self.parameters.parameter['UB'], self.parameters.parameter['Dimension'])
            elif self.dtype is binary:
                self.values = np.random.choice([0, 1], size=(self.parameters.parameter['Dimension']), p=[.5, .5])
            else:
                self.values = np.random.uniform(self.parameters.parameter['LB'], self.parameters.parameter['UB'], self.parameters.parameter['Dimension'])

            #self.evaluate()
        except Exception as err:
            self.fitness = float("inf")
            log.critical(err)

    def evaluate(self):
        print("Starting to evaluate the item at {}".format(time.strftime("%d-%m-%Y %H:%M", time.gmtime())))
        self.fitness = self.function.eval(self.values)
        print("Ending to evaluate the item at {}".format(time.strftime("%d-%m-%Y %H:%M", time.gmtime())))

    def __add__(self, other):
        item = Item(self.parameters, self.function, self.dtype)
        if isinstance(other, Item):
            item.values = self.values + other.values
        else:
            item.values = self.values + other
        return item

    def __radd__(self, other):
        item = Item(self.parameters, self.function, self.dtype)
        if isinstance(other, Item):
            item.values = self.values + other.values
        else:
            item.values = self.values + other
        return item

    def __iadd__(self, other):
        if isinstance(other, Item):
            self.values += other.values
        else:
            self.values += other

    def __sub__(self, other):
        item = Item(self.parameters, self.function, self.dtype)
        if isinstance(other, Item):
            item.values = self.values - other.values
        else:
            item.values = self.values - other
        return item

    def __rsub__(self, other):
        item = Item(self.parameters, self.function, self.dtype)
        if isinstance(other, Item):
            item.values = self.values - other.values
        else:
            item.values = self.values - other
        return item

    def __isub__(self, other):
        if isinstance(other, Item):
            self.values -= other.values
        else:
            self.values -= other

    def __mul__(self, other):
        item = Item(self.parameters, self.function, self.dtype)
        if isinstance(other, Item):
            item.values = self.values * other.values
        else:
            item.values = self.values * other
        return item

    def __rmul__(self, other):
        item = Item(self.parameters, self.function, self.dtype)
        if isinstance(other, Item):
            item.values = self.values * other.values
        else:
            item.values = self.values * other
        return item

    def __imul__(self, other):
        if isinstance(other, Item):
            self.values *= other.values
        else:
            self.values *= other

    def __truediv__(self, other):
        item = Item(self.parameters, self.function, self.dtype)
        if isinstance(other, Item):
            item.values = self.values / other.values
        else:
            item.values = self.values / other
        return item

    def __rdiv__(self, other):
        item = Item(self.parameters, self.function, self.dtype)
        if isinstance(other, Item):
            item.values = self.values / other.values
        else:
            item.values = self.values / other
        return item

    def __idiv__(self, other):
        if isinstance(other, Item):
            self.values /= other.values
        else:
            self.values /= other

    def __lt__(self, item):
        return self.fitness < item.fitness

    def __le__(self, item):
        return self.fitness <= item.fitness

    def __eq__(self, item):
        return self.fitness == item.fitness

    def __hash__(self):
        return hash(self.fitness)

    def __str__(self):
        return "{} - {}".format(self.fitness, self.values)
