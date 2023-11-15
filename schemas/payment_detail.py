class PaymentDetail:
    def __init__(
        self,
        nro_cuota,
        saldo_inicial,
        interes,
        cuota_fija,
        amortizacion,
        pago_seguro_desgravamen,
        pago_seguro_vehicular,
        portes,
        saldo_final,
        flujo,
    ):
        self.nro_cuota = nro_cuota
        self.saldo_inicial = saldo_inicial
        self.interes = interes
        self.cuota_fija = cuota_fija
        self.amortizacion = amortizacion
        self.pago_seguro_desgravamen = pago_seguro_desgravamen
        self.pago_seguro_vehicular = pago_seguro_vehicular
        self.portes = portes
        self.saldo_final = saldo_final
        self.flujo = flujo