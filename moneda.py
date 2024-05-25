class Moneda:
    def __init__(self, nombre_moneda, monto, roi,estado):
        self.NombreMoneda = nombre_moneda
        self.Monto = monto
        self.ROI = roi
        self.Estado =estado

    def __str__(self):
        return f"Nombre de la Moneda: {self.NombreMoneda}, Monto: {self.Monto}, ROI: {self.ROI} , Estado: {self.Estado}"

    def __repr__(self):
        return f"Moneda({self.NombreMoneda}, {self.Monto}, {self.ROI} , {self.Estado})"
