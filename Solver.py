import numpy as np

#Ensamblaje
def AssembleStiffnessMatrix(model,dofData) :

    # extraer la informacion de los DOF
    dofCount = dofData["DOFCount"]

    # Inicializar la matriz de rigidez
    K = np.full((dofCount,dofCount),0.0)

    # Extraer la lista de barras a ensamblar su matriz de rigidez
    bars = model["Bars"]

    for bar in bars :
        barMatrices = bar["BarMatrices"]
        barDOF = bar["BarDOF"]
        ke = barMatrices["k"]
        Te = barMatrices["T"]

        # Matriz de rigidez Global
        Ke = Te.transpose() @ ke @ Te

        # Ensamblamos esta barra
        for i in range(0,Ke.shape[0]) :
            ii = barDOF[i]
            for j in range(0,Ke.shape[1]) :
                jj = barDOF[j]
                K[ii,jj] += Ke[i,j]

    dofU = dofData["UnknownDOFCount"]

    K11 = K[0    : dofU     , 0    : dofU    ]
    K12 = K[0    : dofU     , dofU : dofCount]
    K21 = K[dofU : dofCount , 0    : dofU    ]
    K22 = K[dofU : dofCount , dofU : dofCount]

    return {"K11" : K11,
            "K12" : K12,
            "K21" : K21,
            "K22" : K22}


def AssembleElementForcesVector(model,dofData) :

    # extraer la informacion de los DOF
    dofCount = dofData["DOFCount"]
    dofU = dofData["UnknownDOFCount"]

    QF = np.full((dofCount,1),0.0)

    # Extraer la lista de barras a ensamblar su matriz de rigidez
    bars = model["Bars"]

    for bar in bars :
        if bar.get("qF") is not None :
            barMatrices = bar["BarMatrices"]
            barDOF = bar["BarDOF"]
            qF = bar["qF"]
            Te = barMatrices["T"]
            QFe = Te.transpose() @ qF
            for i in range(0,QFe.shape[0]) :
                ii = barDOF[i]
                QF[ii,0] += QFe[i,0]

    # Particionarlo
    QF1 = QF[0    : dofU     , 0:1]
    QF2 = QF[dofU : dofCount , 0:1]

    return {"QF1" : QF1,
            "QF2" : QF2}


def AssembleForceVector(model,dofData) :

    dofCount       = dofData["DOFCount"]
    dofU           = dofData["UnknownDOFCount"]
    dofArray       = dofData["DOFArray"]
    nodeNumberList = dofData["NodeNumberList"]

    Q = np.full((dofCount,1),0.0)

    nodalForces = model["NodalForces"]
    keys = ["FX", "FY", "MZ"]
    for nodalForce in nodalForces :
        nodeID = nodalForce["NodeID"]
        row = nodeNumberList.index(nodeID)
        for i in range(0,3) :
            value = nodalForce[keys[i]]
            dof = dofArray[row,i]
            Q[dof,0] += value

    Q1 = Q[0    : dofU     , 0 : 1]
    Q2 = Q[dofU : dofCount , 0 : 1]

    return {"Q1" : Q1,
            "Q2" : Q2}

def SolveDisplacements(K,QF,Q,Dk) :

    K11 = K["K11"]
    K12 = K["K12"]
    QF1 = QF["QF1"]
    Q1  = Q["Q1"]

    Du = np.linalg.inv(K11) @ ( Q1 - QF1 - K12 @ Dk )

    return Du