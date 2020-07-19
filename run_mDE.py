from Tools import arguments
from MED.Component import EvaluateComponent
from MED import readFile, element_cov
from Metaheuristics.mDE import *
from Metaheuristics.Run import *
import multiprocessing
import logging as log
import pickle


if __name__ == "__main__":
    try:
        # reads commandline arguments
        arg = arguments()

        parameters = {"Population": 6,
                      "Function_Calls": 10000,
                      "Dimension": 10,
                      "LB": -100,
                      "UB": 100,
                      "F": 0.7,
                      "Cr": 0.9,
                      "Restart": 5,
                      "Elitism": 5}

        # set the log level
        if arg['log'] == 'debug':
            logLevel = log.DEBUG
        elif arg['log'] == 'critical':
            logLevel = log.CRITICAL
        elif arg['log'] == 'error':
            logLevel = log.ERROR
        elif arg['log'] == 'fatal':
            logLevel = log.FATAL
        else:
            logLevel = log.INFO

        MEDParameters = readFile(arg["input"])
        DEParameters = readFile(arg["config"])
        parameters.update(MEDParameters)
        parameters.update(DEParameters)
        parameters["Population"] = multiprocessing.cpu_count()
        parameters["Dimension"] = (len(parameters["Atoms"])-1)*3
        parameters["LB"] = 0
        parameters["UB"] = max([element_cov[item] for item in parameters["Atoms"][1:]])*2
        de = mDEBest1
        med = EvaluateComponent(parameters)
        run = Run("MED", de, parameters, med, loglevel=logLevel)

        run.execute()

        if "binary" in arg:
            with open(arg["binary"], "wb") as bfp:
                pickle.dump(run.results, bfp)

        results = {}
        for result in run.results:
            #print("---------------------------------\n")
            #print(EvaluateComponent.convert(result))
            if result.fitness not in results:
                results[result.fitness] = result

        if "output" in arg:
            with open(arg["output"], "w") as fp:
                cont = 0
                for result in sorted(results.keys())[::-1]:
                    fp.write("---------------------------------\n")
                    fp.write(EvaluateComponent.convert(result))
                    fp.write("\n")

                    cont += 1
                    if cont >= parameters["NumberOfConfigurations"]:
                        break

    except Exception as Err:
        print(Err)
