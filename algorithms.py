# Cambios de tasa de interes

def from_TNA_to_TEA(tasa_nominal):
    tasa_efectiva_anual = (1 + tasa_nominal / (12*30)) ** (360) - 1
    return tasa_efectiva_anual

def from_TEA_to_TNA(tasa_efectiva_anual):
    tasa_nominal = 12*30 * ((1 + tasa_efectiva_anual) ** (1 / 360) - 1)
    return tasa_nominal

def changing_TEA(tasa_efectiva_anual, payment_periods):
    nueva_tasa_efectiva = (1 + tasa_efectiva_anual) ** (payment_periods / 12) - 1
    return nueva_tasa_efectiva

# Hallar cuota fija del metodo frances
def get_fixed_fee(total_loan, tasa_efectiva, total_periods):
    fixed_fee = total_loan * ((tasa_efectiva*(1+tasa_efectiva)**total_periods)/((1+tasa_efectiva)**total_periods-1))
    return fixed_fee





