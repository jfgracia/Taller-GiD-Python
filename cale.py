import math

# Esta es una linea de comentarios


# Ejemplo de ciclo

# for i in range(0,10) :
#     if i < 5 :
#       print(i, " es menor que 5")
#     else :
#       print(i," es igual o mayor a 5")

# i = 0
# while i < 10:
#    print(2*i)
#    i = i + 1

# # Diccionarios
# myDict = {"Name" : "Fernando",
#           "Last" : "Gracia",
#           "Sexo" : "Masculino",
#           "Edad" : 25,
#           "Peso" : 70}

# print(myDict)
# print(myDict["Name"])
# print(myDict["Edad"])

def cuadratica(A,B,C) :
    
  disc = B**2 - 4*A*C
    
  if disc < 0 :
    print("Tas bien wey")
    return
    
  x1 = (-B + math.sqrt(disc))/2/A
  x2 = (-B - math.sqrt(disc))/2/A

  return [x1,x2]


sol = cuadratica(2,4,-6)

print(sol)