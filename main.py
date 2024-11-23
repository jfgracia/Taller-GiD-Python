import IOFiles as io
import Routines as rt
import Solver as sl

import numpy as np
import sys

dataFileName    = ""
logFileName     = ""
resultsFileName = ""
message         = ""

# Lectura del modelo
GiD = True
if(len(sys.argv) > 1) :  # Este prrograma se invoca desde el GiD
    fileName = sys.argv[1]
    dataFileName    = fileName + ".dat"
    logFileName     = fileName + ".log"
    resultsFileName = fileName + ".post.res"
    message = "Este modelo viene de un documento de GiD\n\n"
else : # Este programa se invoca desde Visual Studio
    dataFileName = "Model.dat" #<== Modificar segun el user
    GiD = False
    message = "Este modelo es de prueba y se invoca desde Visual Studio\n\n"

io.reportMessage(logFileName,message,GiD,"w")


# Lectura del modelo
model = io.ReadDataFile(dataFileName)
###
message = "Modelo Leido\n"
message = message + "Nodos:               " + str(len(model["Nodes"]))       + "\n"
message = message + "Barras:              " + str(len(model["Bars"]))        + "\n"
message = message + "Materiales:          " + str(len(model["Materials"]))   + "\n"
message = message + "Propiedades:         " + str(len(model["Properties"]))  + "\n"
message = message + "Apoyos:              " + str(len(model["Restrictions"]))+ "\n"
message = message + "Fuerzas Nodales:     " + str(len(model["NodalForces"])) + "\n"
message = message + "Fuerzas Elementales: " + str(len(model["BarForces"]))   + "\n"
message = message + "\n\n"
io.reportMessage(logFileName,message,GiD)

# Numeracion de los GDL
dofData = rt.GenerateDOF(model)
###
message = "Calculo de grados de libertad\n"
message = message + "GDL Total:          " + str(dofData["DOFCount"])        + "\n"
message = message + "GDL Desconocidos:   " + str(dofData["UnknownDOFCount"]) + "\n"
message = message + "\n\n"
io.reportMessage(logFileName,message,GiD)

# Generacion de las matrices elementales
rt.GenerateElementsDOF(model,dofData)
rt.GenerateElementMatrices(model,dofData)
rt.GenerateElementFixedEndForces(model)
###
message = "Generacion de matriz de rigidez...     OK\n"
message = message + "\n\n"
io.reportMessage(logFileName,message,GiD)

# Ensamblaje
K = sl.AssembleStiffnessMatrix(model,dofData)
###
message = "Ensamble de matriz de rigidez...       OK\n"
message = message + "\n\n"
io.reportMessage(logFileName,message,GiD)

QF = sl.AssebembleElementForcesVector(model,dofData)
###
message = "Ensamble de fuerzas elementales...     OK\n"
message = message + "\n\n"
io.reportMessage(logFileName,message,GiD)

Q = sl.AssembleForceVector(model,dofData)
###
message = "Ensamble de fuerzas nodales...         OK\n"
message = message + "\n\n"
io.reportMessage(logFileName,message,GiD)

# Solucion de desplazamientos
dofCount = dofData["DOFCount"]
unknownDOFCount = dofData["UnknownDOFCount"]
Dk = np.full((dofCount-unknownDOFCount,1),0.0)
Du = sl.SolveDisplacements(K,QF,Q,Dk)
D = {"Du" : Du,
     "Dk" : Dk}
###
message = "Solucion de desplazamientos nodales... OK\n"
message = message + "\n\n"
io.reportMessage(logFileName,message,GiD)

# Solucion de reacciones
R = sl.SolveReactions(K,QF,Q,D)
###
message = "Solucion de reacciones...              OK\n"
message = message + "\n\n"
io.reportMessage(logFileName,message,GiD)

# Solucion de fuerzas elementales
sl.SolveElementForces(model,D)
###
message = "Solucion de fuerzas elementales...     OK\n"
message = message + "\n\n"
io.reportMessage(logFileName,message,GiD)

# Salida de datos

