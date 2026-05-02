import control as ctrl

class TransferFunctionEstimator:
    def __init__(self, zeta, wn):
        self.zeta = zeta
        self.wn = wn

    def get_transfer_function(self):
        num = [self.wn**2]
        den = [1, 2*self.zeta*self.wn, self.wn**2]
        return ctrl.TransferFunction(num, den)