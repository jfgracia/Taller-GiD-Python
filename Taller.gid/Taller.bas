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
*elemsnum *elemsConec *MatProp(5) *elemsmat  *elemsmat
*endif
*end materials
*end elem
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
# Supports
# Qty
# NodeNumber    TX(1 or 0)  TY(1 or 0)  RZ(1 or 0)
*set cond Point-Restraints *nodes
*CondNumEntities
*loop nodes *OnlyInCond
*NodesNum *cond(1) *cond(2) *cond(3)
*end nodes
# Loads - Nodal
# Qty
# NodeNumber    FX(kN)  FY(kN)  MZ(kN-m)
*set cond Point-Loads *nodes
*CondNumEntities
*loop nodes *OnlyInCond
*NodesNum *cond(1) *cond(2) *cond(3)
*end nodes
# Load - Member
# Qty
# BarNumber a(m)    Fa(kN/m)    b(m)    Fb(kN/m)
*set cond Line-Loads *elems
*CondNumEntities
*loop elems *OnlyInCond
*elemsnum *cond(1) *cond(2) *cond(3) *cond(4)
*end elems