# Funcion ReadDataFile
#   Funcion que lee un archivo de texto la informacion del modelo
#   y regresa un diccionario con los datos de la estructura
#
#   Entradas:
#       dataFileName    String, que inlcuye el nombre del documento a leer
#
#   Salidas:
#       model           Diccionario con la informacion del modelo con los keys
#                       "Nodes"   
#                       "Bars"  
#                       "Materials" 
#                       "Properties"
#                       "Restrictions"
#                       "NodalForces"
#                       "BarForces"

def ReadDataFile(dataFileName) :

    with open(dataFileName,"r") as inputFile:

        #Lectura de nodos
        nodes = []

        #Leer 3 lineas de info
        for _ in range(0,3) :
            spare = inputFile.readline()


        nodeCount = int(inputFile.readline().split()[0])
        # NodeNumber CoordX(m) CoordY(m)
        for _ in range(nodeCount) :
            aLine = inputFile.readline().split()
            node = {"Number" : int(aLine[0]),
                    "X"      : float(aLine[1]),
                    "Y"      : float(aLine[2])}
            nodes.append(node)

        #Lectura de barras
        bars = []

        #Leer 3 lineas de info
        for _ in range(0,3) :
            spare = inputFile.readline()

        barCount = int(inputFile.readline().split()[0])
        # BarNumber Node1 Node2 Type Property Material
        for _ in range(barCount) :
            aLine = inputFile.readline().split()
            bar = {"ID"         : int(aLine[0]),
                   "Node1"      : int(aLine[1]),
                   "Node2"      : int(aLine[2]),
                   "Type"       : aLine[3], #TRUSS o FRAME
                   "PropertyID" : int(aLine[4]),
                   "MaterialID" : int(aLine[5])}
            bars.append(bar)

        #Lectura de materiales
        materials = []

        #Leer 3 lineas de info
        for _ in range(0,3) :
            spare = inputFile.readline()
        
        matCount = int(inputFile.readline().split()[0])
        # MatNumber Name E(GPa) Poiss Densidad(kg/m3)
        for _ in range(matCount) :
            aLine = inputFile.readline().split()
            material = {"ID"        : int(aLine[0]),
                        "Name"      : aLine[1],
                        "E"         : float(aLine[2]),
                        "nu"        : float(aLine[3]),
                        "Density"   : float(aLine[4])} 
            materials.append(material)

        #Lectura de propiedades
        properties = []

        #Leer 3 lineas de info
        for _ in range(0,3) :
            spare = inputFile.readline()

        propCount = int(inputFile.readline().split()[0])
        # PropNumber Name A(mm2) I(E06 mm4)
        for _ in range(propCount) :
            aLine = inputFile.readline().split()
            property = {"ID"       : int(aLine[0]),
                        "Name"     : aLine[1],
                        "A"        : float(aLine[2]),
                        "I"        : float(aLine[3]),}
            properties.append(property)

        # Lectura de restricciones nodales
        restrictions = []

        #Leer 3 lineas de info
        for _ in range(0,3) :
            spare = inputFile.readline()

        restCount = int(inputFile.readline().split()[0])
        # NodeNumber    TX(1 or 0)  TY(1 or 0)  RZ(1 or 0)
        for _ in range(restCount) :
            aLine = inputFile.readline().split()
            restriction = {"Node"  : int(aLine[0]),
                           "TX"    : int(aLine[1]),
                           "TY"    : int(aLine[2]),
                           "RZ"    : int(aLine[3])}
            restrictions.append(restriction)

        # Lectura de fuerzas nodales
        nodalForces = []

        #Leer 3 lineas de info
        for _ in range(0,3) :
            spare = inputFile.readline()

        nodalForceCount = int(inputFile.readline().split()[0])
        # NodeNumber    FX(kN)  FY(kN)  MZ(kN-m)
        for _ in range(nodalForceCount) :
            aLine = inputFile.readline().split()
            nodalForce = {"NodeID" : int(aLine[0]),
                          "FX"     : float(aLine[1]),
                          "FY"     : float(aLine[2]),
                          "MZ"     : float(aLine[3])}
            nodalForces.append(nodalForce)

        # Lectura de fuerzas en barras
        barForces = []

        #Leer 3 lineas de info
        for _ in range(0,3) :
            spare = inputFile.readline()

        barForceCount = int(inputFile.readline().split()[0])
        # BarNumber a(m)    Fa(kN/m)    b(m)    Fb(kN/m)
        for _ in range(barForceCount) :
            aLine = inputFile.readline().split()
            barForce = {"BarID"  : int(aLine[0]),
                        "a"      : float(aLine[1]),
                        "wa"     : float(aLine[2]),
                        "b"      : float(aLine[3]),
                        "wb"     : float(aLine[4])} 
            barForces.append(barForce)  

        # Diccionario con todo el modelo
        model = {"Nodes"        : nodes,
                 "Bars"         : bars,
                 "Materials"    : materials,
                 "Properties"   : properties,
                 "Restrictions" : restrictions,
                 "NodalForces"  : nodalForces,
                 "BarForces"    : barForces}

    return model