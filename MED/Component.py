from Metaheuristics import Function
import numpy as np
import subprocess as sp
import time, os
import logging as log
from MED import center


class EvaluateComponent(Function):
    """
    Fitness Function
    """
    def __init__(self, parameters):
        self.parameters = parameters

    def eval(self, element):
        try:
            component = Gaussian(self.parameters, element)
            return component.getEnergy()
        except Exception as Err:
            log.critical(Err)
            return np.array([]), float("inf")

    def convert(Item):
        try:
            strOut = "Energy {}\n".format(Item.fitness)
            positions = np.reshape(Item.values, (len(Item.parameters.parameter["Atoms"]) - 1, 3))
            strOut += "{}{:12.4f}{:12.4f}{:12.4f}\n".format(Item.parameters.parameter["Atoms"][0], 0, 0, 0)
            for x in range(1, len(Item.parameters.parameter["Atoms"])):
                strOut += "{}{:12.4f}{:12.4f}{:12.4f}\n".format(Item.parameters.parameter["Atoms"][x],
                                                                positions[x - 1][0], positions[x - 1][1],
                                                                positions[x - 1][2])
            return strOut
        except Exception as Err:
            log.critical(Err)
            return ""


class Gaussian:
    def __init__(self, parameters, values):
        self.parameters = parameters
        self.values = values
        self.energy = 0.0
        self.file = None

    def getEnergy(self):
        try:
            self.saveFile()
            self.executeFile()

            self.values, self.energy = self.readFile()
            self.values = center(self.values)
        except Exception as Err:
            log.critical("getEnergy {}".format(Err))
            self.energy = float("inf")

        self.removeFile()
        return self.energy
        #return self.values, self.energy

    def saveFile(self):
        try:
            if not os.path.exists("tmp"):
                os.makedirs("tmp")

            self.file = "tmp/Component{}".format(time.time())
            with open(self.file + ".inp", "w") as fp:
                fp.write("%nproc={}\n".format(self.parameters["NProc"]))
                fp.write("#{}/{} opt scf=qc\n".format(self.parameters["Method"],
                                                      self.parameters["Basis"]))
                fp.write("\nECD: Generated Input\n\n")
                fp.write("{} {}\n".format(self.parameters["Charge"], self.parameters["Mult"]))
                positions = np.reshape(self.values, (len(self.parameters["Atoms"]) - 1, 3))
                fp.write("{}{:12.4f}{:12.4f}{:12.4f}\n".format(self.parameters["Atoms"][0], 0, 0, 0))
                for x in range(1, len(self.parameters["Atoms"])):
                    fp.write("{}{:12.4f}{:12.4f}{:12.4f}\n".format(self.parameters["Atoms"][x], positions[x - 1][0], positions[x - 1][1], positions[x - 1][2]))

                fp.write("\n")
        except Exception as Err:
            log.critical("saveFile {}".format(Err))
            raise Err

    def executeFile(self):
        try:
            p = sp.Popen(self.parameters["Program"] + " " + self.file + ".inp", shell=True, stdout=sp.PIPE,
                         stderr=sp.PIPE)
            p.wait()
        except Exception as Err:
            log.critical("executeFile {}".format(Err))
            raise Exception

    def readFile(self):
        try:
            values = []
            cont = 0
            with open(self.file + ".log", 'r') as fp:
                for lines in fp:
                    if cont > 4:
                        if "----" in lines.strip():
                            cont = 0
                        else:
                            value = [x for x in lines.replace("\n", "").split(" ") if x != '']
                            values.append(np.asarray(np.array(value[3:]), dtype=float))
                        continue

                    if cont > 0:
                        cont += 1
                        continue

                    if "Standard orientation:" in lines.strip():
                        cont += 1
                        continue

                    if "SCF Done" in lines.strip():
                        for value in lines.split(" "):
                            try:
                                return values, float(value)
                            except Exception:
                                pass

            return values, float("inf")
        except Exception as Err:
            log.critical("readFile {}".format(Err))
            return np.array([]), float("inf")

    def removeFile(self):
        try:
            os.remove(self.file + ".inp")
            os.remove(self.file + ".log")
        except:
            pass
