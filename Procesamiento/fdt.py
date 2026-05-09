import control as ctrl

class Estimador_FDT:
    def __init__(self, zeta, wn):
        self.zeta = zeta
        self.wn = wn

    def Obtener_funcion_transferencia(self):
        num = [self.wn**2]
        den = [1, 2*self.zeta*self.wn, self.wn**2]
        return ctrl.TransferFunction(num, den)