# Nodes
# Qty
# NodeNumber CoordX(m) CoordY(m)
*npoin
*loop nodes
*NodesNum *NodesCoord(1) *NodesCoord(2)
*end nodes
# Barras
# Qty
# BarNumber Node1 Node2 Type Property Material
*nelem
*loop elems
*loop materials
*if(matnum()==elemsmat)
*elemsnum *elemsConec *MatProp(5) *elemsmat *elemsmat
*endif
*end materials
*end elems
# Materiales
# Qty
# MatNumber Name E(GPa) Poiss Densidad(kg/m3)
*nmats
*loop materials
*matnum() *MatProp(1) *MatProp(2) *MatProp(3) *MatProp(4)
*end materials
# Propiedades
# Qty
# PropNumber Name A(mm2) I(E06 mm4)
*nmats
*loop materials
*matnum() *MatProp(6) *MatProp(7) *MatProp(8)
*end materials