import os, json, sys
import logging as log
import numpy as np


element_cov = {"X": 0.50, "H": 0.32, "He": 0.93, "Li": 1.23, "Be": 0.90, "B": 0.82, "C": 0.77, "N": 0.75, "O": 0.73, "F": 0.72, "Ne": 0.71, "Na": 1.54, "Mg": 1.36, "Al": 1.18, "Si": 1.11, "P": 1.06, "S": 1.02, "Cl": 0.99, "Ar": 0.98, "K": 2.03, "Ca": 1.74, "Sc": 1.44, "Ti": 1.32, "V": 1.22, "Cr": 1.18, "Mn": 1.17, "Fe": 1.17, "Co": 1.16, "Ni": 1.15, "Cu": 1.17, "Zn": 1.25, "Ga": 1.26, "Ge": 1.22, "As": 1.20, "Se": 1.16, "Br": 1.14, "Kr": 1.12, "Rb": 2.16, "Sr": 1.91, "Y": 1.62, "Zr": 1.45, "Nb": 1.34, "Mo": 1.30, "Tc": 1.27, "Ru": 1.25, "Rh": 1.25, "Pd": 1.28, "Ag": 1.34, "Cd": 1.48, "In": 1.44, "Sn": 1.41, "Sb": 1.40, "Te": 1.36, "I": 1.33, "Xe": 1.31, "Cs": 2.35, "Ba": 1.98, "La": 1.69, "Ce": 1.65, "Pr": 1.65, "Nd": 1.64, "Pm": 1.63, "Sm": 1.62, "Eu": 1.85, "Gd": 1.61, "Tb": 1.59, "Dy": 1.59, "Ho": 1.58, "Er": 1.57, "Tm": 1.56, "Yb": 1.74, "Lu": 1.56, "Hf": 1.44, "Ta": 1.34, "W": 1.30, "Re": 1.28, "Os": 1.26, "Ir": 1.27, "Pt": 1.30, "Au": 1.34, "Hg": 1.49, "Tl": 1.48, "Pb": 1.47, "Bi": 1.46, "Po": 1.46, "At": 1.45, "Rn": 1.90, "Fr": 1.00, "Ra": 1.00, "Ac": 1.00, "Th": 1.65, "Pa": 1.00, "U": 1.42, "Np": 1.50, "Pu": 1.50, "Am": 1.50, "Cm": 1.50, "Bk": 1.50, "Cf": 1.50, "Es": 1.50, "Fm": 1.50, "Md": 1.50, "No": 1.50, "Lr": 1.50}


def centerAtoms(Positions):
    if len(Positions) == 0:
        return []
    positions = sorted(Positions, key=lambda k: k["Atom"])
    center = np.array(positions[0]["Pos"])
    for item in positions:
        item["Pos"] -= center
    return positions


def center(Positions):
    if len(Positions) == 0:
        return np.array([])
    positions = np.array([])
    for item in range(1, len(Positions)):
        positions = np.concatenate((positions, Positions[item] - Positions[0]))
    return positions


def readFile(file="GEGA.inp"):
    if not os.path.exists(file):
        print("The file " + file + " doesn't exists")
        sys.exit(2)

    if ".inp" in file:
        return readGEGA(file)
    if ".json" in file:
        return readJSON(file)


def readJSON(file="GEGA.json"):
    # parameter = {}
    try:
        with open(file, 'r') as fp:
            return json.load(fp)
    except Exception:
        raise Exception


def readGEGA(file="GEGA.inp"):
    parameter = {}
    try:
        with open(file, 'r') as fp:
            # Obtains the values from the file, removing the lines that start with : and the empty ones.
            cont = [value.strip() for value in fp if ((not value.strip()[:1] == ":") and (len(value.strip()) > 0))]
            pos = 0
            for i in range(len(cont)):
                if "Cycles:" in cont[i]:
                    values = cont[i].split(":")[1].split("/")
                    parameter["MaxOpt"] = int(values[0])
                    parameter["MaxSCF"] = int(values[1])
                    pos = i + 1
                    break
            for i in range(pos, len(cont)):
                if "NProc:" in cont[i]:
                    parameter["NProc"] = int(cont[i].split(":")[1])
                    pos = i + 1
                    break
            for i in range(pos, len(cont)):
                if "Program:" in cont[i]:
                    parameter["Program"] = cont[i].split(":")[1].strip()
                    pos = i + 1
                    break
            for i in range(pos, len(cont)):
                if "NumberOfConfigurations:" in cont[i]:
                    parameter["NumberOfConfigurations"] = int(cont[i].split(":")[1])
                    pos = i + 1
                    break
            parameter["Method"], parameter["Basis"] = cont[pos].split(" ")
            pos += 1
            values = cont[pos].split(" ")
            parameter["Charge"] = int(values[0])
            parameter["Mult"] = int(values[1])
            Atoms = []
            for i in range(pos + 1, len(cont)):
                if "---" in cont[i]:
                    break

                values = cont[i].split(" ")
                for atom in range(int(values[1])):
                    Atoms.append(values[0])

            pos = i + 1
            Positions = []
            for i in range(pos, len(cont)):
                values = [x for x in cont[i].split(" ") if x != '']
                position = {"Atom": values[0],
                            "Pos": np.array([float(val) for val in values[1:4]])}
                Positions.append(position)

            parameter["Atoms"] = sorted(Atoms)
            parameter["Positions"] = centerAtoms(Positions)  # sorted(Positions, key=lambda k: k["Atom"])
        return parameter

    except Exception:
        raise Exception
