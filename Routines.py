import numpy as np
import math

#   funcion GenerateDOF
#   Calcula los grados de libertad nodales, primero los 
#   desconocidos, al final los conocidos
#
#   Entrada:    model (Diccionario del modelo)
#
#   Salida:     dofData
#               diccionario con los grados de libertad
#               keys
#               "DOFCount"        : Numero total de grados de libertad
#               "UnknownDOFCount" : Grados de libertad desconocidos
#               "DOFArray"        : Matriz con numero de renglones el numero de nodos
#                                   y 3 columnas representado el GDLx, GDLy y GDLrz
#               "NodeNumberList"  : Lista con numero de nodos

DEFAULT_TOLERANCE = 0.00001

def gt(a,b,tolerance = DEFAULT_TOLERANCE) :
    return a > b + tolerance

def ge(a,b,tolerance = DEFAULT_TOLERANCE) :
    return a >= b + tolerance

def eq(a,b,tolerance = DEFAULT_TOLERANCE) :
    return abs(a-b) <= tolerance

def GenerateDOF(model) :

    dofList = []
    nodeNumberList = []

    # Extraer los nodos y las restricciones del modelo
    nodes = model["Nodes"]
    restrictions = model["Restrictions"]

    # Inicializar el arreglo de nodos y DOF
    for node in nodes:
        nodeDOF = [-2, -2, -2]
        nodeNumberList.append(node["Number"])
        dofList.append(nodeDOF)


    # Recorrer la lista de DOF para marcar los restringidos con -1
    keys = ["TX", "TY", "RZ"]
    for restriction in restrictions:
        nodeNumber = restriction["Node"]
        row = nodeNumberList.index(nodeNumber)
        for key in keys:
            value = restriction[key]
            if value == 1: # Tengo restriccion
                col = keys.index(key)
                dofList[row][col] = -1

    # Numerar los DOF desconocidos
    dof = 0
    for nodeDOF in dofList: #Lista de los 3 DOF por nodo
        for col in range(0,3) :
            if nodeDOF[col] == -2:
                nodeDOF[col] = dof
                dof += 1
    unknownDOFCount = dof

    # Numerar los DOF conocidos
    for nodeDOF in dofList: #Lista de los 3 DOF por nodo
        for col in range(0,3) :
            if nodeDOF[col] == -1:
                nodeDOF[col] = dof
                dof += 1

    dofData = {"DOFCount"        : dof,
               "UnknownDOFCount" : unknownDOFCount,
               "DOFArray"        : np.array(dofList),
               "NodeNumberList"  : nodeNumberList}

    return dofData

# Rutinas del elemento armadura [k] [T]
#
#         | 1  0 -1  0 |
#    AE/L | 0  0  0  0 |
#         |-1  0  1  0 |
#         | 0  0  0  0 |
def LocalStiffnessMatrix_TRUSS(A,E,L):

    # Inicializar la matrix 4x4 llena de 0
    k = np.full((4,4),0.0)

    # Valores
    EA_L = E*A/L
    k[0,0] =  EA_L
    k[0,2] = -EA_L
    k[2,0] = -EA_L
    k[2,2] =  EA_L

    return k

#         | C  S  0  0 |
#         |-S  C  0  0 |
#         | 0  0  C  S |
#         | 0  0 -S  C |
def TrasnformationMatrix_TRUSS(C,S):

    # Inicializar la matrix 4x4 llena de 0
    T = np.full((4,4),0.0)

    T[0,0] = C; T[0,1] = S
    T[1,0] =-S; T[1,1] = C
    T[2,2] = C; T[2,3] = S
    T[3,2] =-S; T[3,3] = C

    return T

def Matrices_TRUSS(A,E,L,C,S) :

    k = LocalStiffnessMatrix_TRUSS(A,E,L)
    T = TrasnformationMatrix_TRUSS(C,S)

    barMatrices = {"k"  : k,
                   "T"  : T}

    return barMatrices

# Rutinas del elemento Marco [k] [T]

def LocalStiffnessMatrix_FRAME(A,E,I,L):

     # Inicializar la matrix 6x6 llena de 0
    k = np.full((6,6),0.0)

    # Componentes axiales
    EA_L = E*A/L
    k[0,0] =  EA_L; k[0,3] = -EA_L
    k[3,0] = -EA_L; k[3,3] =  EA_L 

    # Componentes flexión
    __2EI_L   = 2.0 * E * I / L
    __4EI_L   = 2.0 * __2EI_L
    __6EI_L2  = (__2EI_L + __4EI_L) / L
    _12EI_L3  = 2 * __6EI_L2 / L

    k[1,1] =  _12EI_L3; k[1,2] =  __6EI_L2; k[1,4] = -_12EI_L3; k[1,5] =  __6EI_L2
    k[2,1] =  __6EI_L2; k[2,2] =  __4EI_L ; k[2,4] = -__6EI_L2; k[2,5] =  __2EI_L
    k[4,1] = -_12EI_L3; k[4,2] = -__6EI_L2; k[4,4] =  _12EI_L3; k[4,5] = -__6EI_L2
    k[5,1] =  __6EI_L2; k[5,2] =  __2EI_L ; k[5,4] = -__6EI_L2; k[5,5] =  __4EI_L

    return k

def TrasformationMatrix_FRAME(C,S):

     # Inicializar la matrix 6x6 llena de 0
    T = np.full((6,6),0.0)

    # Valores
    T[0,0] =  C; T[0,1] =  S
    T[1,0] = -S; T[1,1] =  C
    T[2,2] =  1.0
    T[3,3] =  C; T[3,4] =  S
    T[4,3] = -S; T[4,4] =  C
    T[5,5] =  1.0

    return T

def Matrices_FRAME(A,E,I,L,C,S):

    k = LocalStiffnessMatrix_FRAME(A,E,I,L)
    T = TrasformationMatrix_FRAME(C,S)

    barMatrices = {"k": k,
                   "T": T}

    return barMatrices

# Rutina que integra numericamente el caso de
# una carga uniforme con magnitud variable desde a
# hasta b (Caso General)
def FixedEndMoment_FRAME(L,a,wa,b,wb):

    # Inicializar el vector qF de 6x1
    qF = np.full((6,1),0.0)

    # Verficaciones de seguridad
    if eq(a,0.0) and eq(b,0.0) : # Caso especial para definir que es en toda la longitud
        b = L
    elif ge(a,b) :
        print("Error en carga, a >=b")
        return qF
    elif gt(b,L) :
        print("Error en carga, b > L")
        return qF
    
    # Integracion mediante la ley de Booles
    wt = [7.0, 32.0, 12.0, 32.0, 7.0]
    m = (wb-wa)/(b-a)
    MA = 0.0
    MB = 0.0

    for i in range(0,5):
        x = a + float(i) * (b-a) / 4.0
        fA = x * ( (L-x) ** 2.0) * ( m * (x - a) + wa )
        fB = (x ** 2.0) * (L-x)  * ( m * (x - a) + wa )
        MA = MA + wt[i] * fA
        MB = MB + wt[i] * fB

    MA =  (b-a) * MA / 90.0 / (L ** 2.0)
    MB = -(b-a) * MB / 90.0 / (L ** 2.0)

    # Cortantes
    R1 = wa * (b-a)
    d1 = a + (b-a)/2.0
    R2 = (wb-wa)*(b-a)/2.0
    d2 = a + 2.0 * (b - a) / 3.0
    VB = ( R1*d1 + R2 * d2 - MA - MB) / L
    VA = R1 + R2 - VB

    qF[1,0] = VA
    qF[2,0] = MA
    qF[4,0] = VB
    qF[5,0] = MB

    return qF

# Utilerias

# Generar la lista de DOF en cada barra
# y pegarlas al diccionario de cada barra
def GenerateElementsDOF(model,dofData):

    # extraer la lista de barras del modelo
    bars = model["Bars"]

    # Extraer la lista de nodos y sus DOF
    nodeNumberList = dofData["NodeNumberList"]
    dofArray = dofData["DOFArray"]

    # Recorrido por todas las barras
    for bar in bars :
        barNodes = [ bar["Node1"] , bar["Node2"] ]
        type = bar["Type"]

        barDOF = []
        dofPerBarEnd = 0
        if type == "TRUSS" :
            dofPerBarEnd = 2
        else :
            dofPerBarEnd = 3

        for barNode in barNodes :
            row = nodeNumberList.index(barNode)
            for ii in range(0,dofPerBarEnd) :
                dof = int(dofArray[row,ii])
                barDOF.append(dof)

        bar.update({"BarDOF" : barDOF})

    return

# Generar todas las matrices elementales
# y pegarlas al diccionario de cada barra
def GenerateElementMatrices(model,dofData):

    # extraer la lista de barras
    bars = model["Bars"]

    # extraer el ordemiento de los nodos
    nodeNumberList = dofData["NodeNumberList"]
    
    # extraer del modelo la lista nodos
    # para calcular L, C, S
    nodes = model["Nodes"]

    # extraer la lista de propiedades
    # para extraer A,I
    properties = model["Properties"]

    # extraer la lista de materiales
    # para extraer E
    materials = model["Materials"]

    for bar in bars :
        type = bar["Type"] #TRUSS o FRAME
        barNodes = [ bar["Node1"], bar["Node2"] ]
        xcoord = []
        ycoord = []

        for barNode in barNodes:
            row = nodeNumberList.index(barNode)
            xcoord.append( nodes[row]["X"] )
            ycoord.append( nodes[row]["Y"] )
        
        dx = xcoord[1] - xcoord[0]
        dy = ycoord[1] - ycoord[0]
        L = math.sqrt( dx**2.0 + dy**2.0)
        C = dx / L
        S = dy / L

        propertyID = bar["PropertyID"]
        materialID = bar["MaterialID"]

        barProperty = []
        barMaterial = []

        for property in properties:
            if propertyID == property["ID"] :
                barProperty = property
                break

        for material in materials :
            if materialID == material["ID"] :
                barMaterial = material
                break

        barMatrices = []
        if type == "TRUSS" :
            barMatrices = Matrices_TRUSS(barProperty["A"],
                                         barMaterial["E"],
                                         L, C, S)
        elif type ==  "FRAME" :
            barMatrices = Matrices_FRAME(barProperty["A"],
                                         barMaterial["E"],
                                         barProperty["I"],
                                         L,C,S)

        bar.update({"BarMatrices" : barMatrices})
        bar.update({"Length" : L})

    return

# Generar los vectores de empotramiento perfecto elementales
# y pegarselos al diccionario de la barra
def GenerateElementFixedEndForces(model) :

    # Extraer del modelo la informacion de los bar forces
    barForces = model["BarForces"]

    # Extraer los diccionarios de las barras
    bars = model["Bars"]

    for barForce in barForces :

        barID = barForce["BarID"]
        appliedBarForce = []

        # Buscar la barra en la lista de barras
        for bar in bars :
            if barID == bar["ID"] :
                appliedBarForce = bar
                break
        
        # Este tipo de caras solo funcionan con el FRAME
        if appliedBarForce["Type"] == "FRAME" :
            L  = appliedBarForce["Length"]
            a  =  barForce["a"]
            wa = -barForce["wa"] # Sentido -Y local es positivo en las FixedEndMoment_FRAME
            b  =  barForce["b"]
            wb = -barForce["wb"] #  Sentido -Y local es positivo en las FixedEndMoment_FRAME
            qF = FixedEndMoment_FRAME(L,a,wa,b,wb)

            # Tiene o no tiene qF este barra?
            if appliedBarForce.get("qF") is not None: # Sumarlo
                prev_qf = appliedBarForce["qF"]
                qF = qF + prev_qf
                appliedBarForce["qF"] = qF
            else :
                appliedBarForce.update({"qF" : qF})
            
        else :
            print("Aviso: Las cargas sobre barras solo aplican para elementos tipo FRAME")
            print("La carga será ignorada")

    return


