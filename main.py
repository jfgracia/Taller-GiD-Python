import IOFiles as io
import Routines as rt

# Lectura del modelo
archivo = "Model.dat"
model = io.ReadDataFile(archivo)

# Numeracion de los GDL
dofData = rt.GenerateDOF(model)

# Generacion de las matrices elementales
print(rt.FixedEndMoment_FRAME(4,0.1,10,2,15))
rt.GenerateElementsDOF(model,dofData)
rt.GenerateElementMatrices(model,dofData)
rt.GenerateElementFixedEndForces(model)
print("caca")
# Ensamblaje

# Solucion de desplazamientos

# Solucion de reacciones

# Solucion de fuerzas elementales

# Salida de datos

