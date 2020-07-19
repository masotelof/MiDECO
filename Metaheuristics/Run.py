from Metaheuristics import *
import logging as log
import copy


class Run:
    def __init__(self, name, metaheuristic, parameters, function, loglevel=log.CRITICAL):
        if not issubclass(metaheuristic, Metaheuristic):
            raise Exception('')

        if not isinstance(parameters, dict):
            raise Exception('')

        if not isinstance(function, Function):
            raise Exception('')

        self.name = name
        self.metaheuristic = metaheuristic
        self.parameters = Parameters(parameters)
        self.function = function
        self.loglevel = loglevel
        self.results = []

    def execute(self):
        try:
            log.basicConfig(level=self.loglevel, format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

            metaheuristic = self.metaheuristic(self.name, copy.copy(self.parameters), self.function)
            metaheuristic.run()
            self.results = metaheuristic.items[:]
        except Exception as Err:
            raise Exception(Err)
