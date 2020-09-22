# Micro-differential evolution cluster-optimizer (MiDECO)
The **Micro-differential evolution cluster-optimizer** (MiDECO) is an evolutive framework to model molecules from their atoms.

MiDECO uses a Micro-Differential Evolution (mDE) to optimize the atom position in the molecule,  working in a three-dimensional space.

Gaussian is used to calculate the energy from the molecule proposed and it is used as a fitness function in mDE.

## Usage

It's included a bash file to process all the files inp, is necessary to indicate the directory with the inp files to be processed and thee file with global options.

```
sh execute_all.sh <directory with inp files> <global options files>
```

## Input file

MiDECO needs an input file to specify the parameters to be used in the evolutive process.

The input file usually has the extension inp and it contains the following structure:
-  A line that starts with two points and is empty.
- The cycles to be used in Gaussian.
- The process to be used by each Gaussian instance.
- The Gaussian path.
- The configurations showed by MiDECO.
- Optimization method used by Gaussian.
- Gaussian configuration.
- List with Atoms Symbols and amount to be used.

```
:                        Empty line assumed here
Cycles: 50/50
NProc: 1
Program: /home/usuario/g09/g09
NumberOfConfigurations: 10
B3LYP 3-21G

2 1
C 2
Ge 2
---
```

## Config file

This is a json file with the mDE parameters:
- Population: population size.
- Function_Calls: evaluations number
- F: scale factor 
- Cr: crossover probability
- Restart: iterations to restart the population
- Elitism: best items to be conserved 
