# Cambios de tasa de interes

def from_TNA_to_TEA(tasa_nominal):
    tasa_efectiva_anual = (1 + tasa_nominal / (12*30)) ** (360) - 1
    return tasa_efectiva_anual

def from_TEA_to_TNA(tasa_efectiva_anual):
    tasa_nominal = 12*30 * ((1 + tasa_efectiva_anual) ** (1 / 360) - 1)
    return tasa_nominal

def changing_TE(TEA, payment_frequency):
    changed_TE = (1 + TEA) ** (payment_frequency / 12) - 1
    return changed_TE


# Ajustar el seguro anual con la nueva frecuencia de pago
def get_desgravamen_insurance_amount(desgravamen_percent, funding_amount, period_frequency):
    desgravamen_amount = desgravamen_percent * funding_amount * period_frequency
    return desgravamen_amount

def get_vehicle_insurance_amount(vehicle_insurance_percent, vehicle_price, period_frequency):
    vehicule_insurance = vehicle_price * (vehicle_insurance_percent/(12/period_frequency))
    return vehicule_insurance

# Hallar cuota fija del metodo frances
def get_fixed_fee(funding_amount, tasa_efectiva, total_periods, desgravamen_insurance_percent):
    tasa_efectiva += desgravamen_insurance_percent
    fixed_fee = funding_amount * ((tasa_efectiva*(1+tasa_efectiva)**total_periods)/((1+tasa_efectiva)**total_periods-1))
    return fixed_fee

