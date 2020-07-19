from Metaheuristics import *
from threading import Thread
import logging as log
import random


def random_values(items, up, pos=None):
    valores = []
    while len(valores) < items:
        item = random.randint(0, up-1)
        if item not in valores and item is not pos:
            valores.append(item)
    return valores


class mDE(Metaheuristic):
    """
    Differential Evolution
    """

    def __init__(self, name, parameters, function, dtype=float):
        super().__init__(parameters, function, dtype, name=name)

    def run(self):
        try:
            elements = []
            jobs = []
            for i in range(self.parameters.parameter['Population']):
                self.functionCall.addFunctionCall()
                elements.append(DEItem(self.parameters, self.function, self.dtype))
                elements[-1].initialization()
                jobs.append(Thread(target=elements[-1].evaluate()))
                jobs[-1].start()

            for job in jobs:
                job.join()

            best = min(elements)

            self.items.append(best)
            print("{} {} {}".format(self.name, self.functionCall.current, best.fitness))
            log.info("%s %d %f", self.name, self.functionCall.current, best.fitness)

            cont = 0
            while self.functionCall.isAvailable:
                if cont % self.parameters.parameter['Restart']:
                    elements = sorted(elements)[:self.parameters.parameter['Elitism']]
                    jobs = []
                    for i in range(self.parameters.parameter['Population']-self.parameters.parameter['Elitism']):
                        self.functionCall.addFunctionCall()
                        elements.append(DEItem(self.parameters, self.function, self.dtype))
                        elements[-1].initialization()
                        jobs.append(Thread(target=elements[-1].evaluate()))
                        jobs[-1].start()

                    for job in jobs:
                        job.join()

                npop = self.crossover(elements, self.mutate(elements))
                for (i, item) in enumerate(npop):
                    if item < elements[i]:
                        elements[i] = item

                best = min(elements)
                self.items.append(best)

                print("{} {} {}".format(self.name, self.functionCall.current, best.fitness))
                log.info("%s %d %f", self.name, self.functionCall.current, best.fitness)
                cont += 1

        except FunctionCallException:
            pass

        except Exception as Err:
            log.critical(Err)

    def mutate(self, items):
        pass

    def crossover(self, pop, mut):
        npop = []
        jobs = []

        for (itempop, itemmut) in zip(pop, mut):
            self.functionCall.addFunctionCall()
            j = random.randint(0, len(itempop.values))
            values = []
            for (i, item) in enumerate(itempop.values):
                if random.random() <= self.parameters.parameter['Cr'] or i is j:
                    values.append(itemmut.values[i])
                else:
                    values.append(item)

            npop.append(Item(parameter=self.parameters, function=itempop.function, dtype=float, values=np.array(values)))

            jobs.append(Thread(target=npop[-1].evaluate()))
            jobs[-1].start()

        for job in jobs:
            job.join()

        return npop


class mDECurrentRand1(mDE):
    def mutate(self, items):
        npop = []
        for i in range(len(items)):
            self.functionCall.addFunctionCall()
            r1, r2 = random_values(2, len(items), i)
            ind = items[i] + self.parameters.parameter['F'] * (items[r1] - items[r2])
            npop.append(ind)

        return npop


class mDERand1(mDE):
    def mutate(self, items):
        npop = []
        for i in range(len(items)):
            self.functionCall.addFunctionCall()
            r1, r2, r3 = random_values(3, len(items), i)
            ind = items[r1] + self.parameters.parameter['F'] * (items[r2] - items[r3])
            npop.append(ind)

        return npop


class mDERand2(mDE):
    def mutate(self, items):
        npop = []
        for i in range(len(items)):
            self.functionCall.addFunctionCall()
            r1, r2, r3, r4, r5 = random_values(5, len(items), i)
            ind = items[r5] + self.parameters.parameter['F'] * (items[r1] + items[r2] - items[r3] - items[r4])
            npop.append(ind)

        return npop


class mDEBest1(mDE):
    def mutate(self, items):
        npop = []
        best = min(items)
        for i in range(len(items)):
            self.functionCall.addFunctionCall()
            r1, r2, = random_values(2, len(items), i)
            ind = best + self.parameters.parameter['F'] * (items[r1] - items[r2])
            npop.append(ind)

        return npop


class mDEBest2(mDE):
    def mutate(self, items):
        npop = []
        best = min(items)
        for i in range(len(items)):
            self.functionCall.addFunctionCall()
            r1, r2, r3, r4 = random_values(4, len(items), i)
            ind = best + self.parameters.parameter['F'] * (items[r1] + items[r2] - items[r3] - items[r4])
            npop.append(ind)

        return npop


class DEItem(Item):
    """
    Differential Evolution Items
    """
    pass


class DEParameters(Parameters):
    """
    Differential Evolution Parameters
    """
    def __init__(self, param=None):
        super().__init__(param)
        if "F" not in self.parameter:
            self.parameter['F'] = 0.8
        if "Cr" not in self.parameter:
            self.parameter['Cr'] = 0.9
