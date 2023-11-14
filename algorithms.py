from 


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

def get_fixed_fee_pg(
    funding_amount,
    tasa_efectiva,
    total_periods,
    desgravamen_insurance_percent,
    pg_total,
    pg_parcial,
):
    for i in range(pg_total):
        funding_amount += funding_amount * tasa_efectiva
        total_periods -= 1

    total_periods -= pg_parcial
    tasa_efectiva += desgravamen_insurance_percent
    fixed_fee = funding_amount * (
        (tasa_efectiva * (1 + tasa_efectiva) ** total_periods)
        / ((1 + tasa_efectiva) ** total_periods - 1)
    )
    return fixed_fee


# Hallar todos los flujos
def get_all_flujos(
    nro_cuota,
    todos_los_flujos,
    total_periods,
    funding_amount,
    changed_TE,
    fixed_fee,
    degravamen_percent,
    vehicular_insurance_amount,
    pg_total=0,
    pg_parcial=0,
):
    saldo_inicial = funding_amount
    interes = saldo_inicial * changed_TE
    cuota_fija = fixed_fee
    pago_seguro_desgravamen = saldo_inicial * degravamen_percent
    amortizacion = cuota_fija - interes - pago_seguro_desgravamen
    pago_seguro_vehicular = vehicular_insurance_amount
    portes = 10
    saldo_final = saldo_inicial - amortizacion
    flujo = cuota_fija + pago_seguro_vehicular + portes

    if pg_total > 0:
        pg_total -= 1

        saldo_inicial = funding_amount
        interes = saldo_inicial * changed_TE
        cuota_fija = 0
        pago_seguro_desgravamen = saldo_inicial * degravamen_percent
        amortizacion = 0
        pago_seguro_vehicular = vehicular_insurance_amount
        portes = 10
        saldo_final = saldo_inicial + interes
        flujo = cuota_fija + pago_seguro_desgravamen + pago_seguro_vehicular + portes

        payment = PaymentDetail(
            nro_cuota + 1,
            saldo_inicial,
            interes,
            cuota_fija,
            amortizacion,
            pago_seguro_desgravamen,
            pago_seguro_vehicular,
            portes,
            saldo_final,
            flujo,
        )

        todos_los_flujos.append(payment)
        return get_all_flujos(
            nro_cuota + 1,
            todos_los_flujos,
            total_periods,
            saldo_final,
            changed_TE,
            fixed_fee,
            degravamen_percent,
            vehicular_insurance_amount,
            pg_total,
            pg_parcial,
        )

    if pg_parcial > 0:
        pg_parcial -= 1

        saldo_inicial = funding_amount
        interes = saldo_inicial * changed_TE
        cuota_fija = interes
        pago_seguro_desgravamen = saldo_inicial * degravamen_percent
        amortizacion = 0
        pago_seguro_vehicular = vehicular_insurance_amount
        portes = 10
        saldo_final = saldo_inicial
        flujo = cuota_fija + pago_seguro_desgravamen + pago_seguro_vehicular + portes

        payment = PaymentDetail(
            nro_cuota + 1,
            saldo_inicial,
            interes,
            cuota_fija,
            amortizacion,
            pago_seguro_desgravamen,
            pago_seguro_vehicular,
            portes,
            saldo_final,
            flujo,
        )

        todos_los_flujos.append(payment)
        return get_all_flujos(
            nro_cuota + 1,
            todos_los_flujos,
            total_periods,
            saldo_final,
            changed_TE,
            fixed_fee,
            degravamen_percent,
            vehicular_insurance_amount,
            pg_total,
            pg_parcial,
        )

    payment = PaymentDetail(
        nro_cuota + 1,
        saldo_inicial,
        interes,
        cuota_fija,
        amortizacion,
        pago_seguro_desgravamen,
        pago_seguro_vehicular,
        portes,
        saldo_final,
        flujo,
    )

    if nro_cuota < total_periods:
        todos_los_flujos.append(payment)
        return get_all_flujos(
            nro_cuota + 1,
            todos_los_flujos,
            total_periods,
            saldo_final,
            changed_TE,
            fixed_fee,
            degravamen_percent,
            vehicular_insurance_amount,
        )
    else:
        return todos_los_flujos

