import IOFiles as io
import Routines as rt
import Solver as sl

import numpy as np
import sys

# Lectura del modelo
# archivo = "Model.dat"
GiD = True
dataFileName = ""
if len(sys.argv) > 1 : #Este programa se invoca desde GiD
    fileName = sys.argv[1]
    dataFileName = fileName + ".dat"
    print("El modelo viene de un documento en GiD\n\n")
else : #Este programa se invoca desde Visual Studio
    dataFileName = "Model.dat"
    print("El modelo es de prueba y se invoca desde Visual Studio\n\n")

model = io.ReadDataFile(dataFileName)

# Numeracion de los GDL
dofData = rt.GenerateDOF(model)

# Generacion de las matrices elementales
rt.GenerateElementsDOF(model,dofData)
rt.GenerateElementMatrices(model,dofData)
rt.GenerateElementFixedEndForces(model)

# Ensamblaje
K = sl.AssembleStiffnessMatrix(model,dofData)
# K11 = K["K11"]
# K12 = K["K12"]
# K21 = K["K21"]
# K22 = K["K22"]

# np.savetxt("K11.xls",K11,delimiter="\t")
# np.savetxt("K12.xls",K12,delimiter="\t")
# np.savetxt("K21.xls",K21,delimiter="\t")
# np.savetxt("K22.xls",K22,delimiter="\t")

QF = sl.AssebembleElementForcesVector(model,dofData)
#print(QF)

Q = sl.AssembleForceVector(model,dofData)
#print(Q)

# Solucion de desplazamientos
dofCount = dofData["DOFCount"]
unknownDOFCount = dofData["UnknownDOFCount"]
Dk = np.full((dofCount-unknownDOFCount,1),0.0)
Du = sl.SolveDisplacements(K,QF,Q,Dk)
#print(Du)
#D = np.concatenate((Du,Dk))
#print(D)
D = {"Du" : Du,
     "Dk" : Dk}

# Solucion de reacciones
R = sl.SolveReactions(K,QF,Q,D)
print("Calcule las reacciones")
print(R)

# Solucion de fuerzas elementales
sl.SolveElementForces(model,D)
print("Calcule las fuerzas de barras ok")

# Salida de datos

