from schemas.payment_detail import PaymentDetail

def from_TNA_to_TEA(tasa_nominal):
    tasa_efectiva_anual = (1 + tasa_nominal / (12*30)) ** (360) - 1
    return tasa_efectiva_anual

def from_TEA_to_TNA(tasa_efectiva_anual):
    tasa_nominal = 12*30 * ((1 + tasa_efectiva_anual) ** (1 / 360) - 1)
    return tasa_nominal

def changing_TE(TEA, payment_frequency):
    changed_TE = (1 + TEA) ** (payment_frequency / 12) - 1
    return changed_TE

def get_desgravamen_insurance_amount(desgravamen_percent, funding_amount, period_frequency):
    desgravamen_amount = desgravamen_percent * funding_amount * period_frequency
    return desgravamen_amount

def get_vehicle_insurance_amount(anual_vehicle_insurance_percent, vehicle_price, period_frequency):
    vehicle_insurance = vehicle_price * (anual_vehicle_insurance_percent/(12/period_frequency))
    return vehicle_insurance

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
    _portes = 10
):
    saldo_inicial = funding_amount
    interes = saldo_inicial * changed_TE
    cuota_fija = fixed_fee
    pago_seguro_desgravamen = saldo_inicial * degravamen_percent
    amortizacion = cuota_fija - interes - pago_seguro_desgravamen
    pago_seguro_vehicular = vehicular_insurance_amount
    portes = _portes
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
            portes
        )

    if pg_parcial > 0:
        pg_parcial -= 1

        saldo_inicial = funding_amount
        interes = saldo_inicial * changed_TE
        cuota_fija = interes
        pago_seguro_desgravamen = saldo_inicial * degravamen_percent
        amortizacion = 0
        pago_seguro_vehicular = vehicular_insurance_amount
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
            portes
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
            0,
            0,
            portes
        )
    else:
        return todos_los_flujos


def get_VAN(TEA, funding_amount, total_periods, cashflow):
    VAN = funding_amount 
    for i in range(total_periods):
        VAN += (cashflow[i]*-1)/((1+TEA)**(i+1))
    return VAN

def get_TIR(funding_amount, total_periods, cashflow, tolerance=1e-6, max_iterations=1000):
    rate_low = 0.0
    rate_high = 1.0
    irr = 0.0

    for _ in range(max_iterations):
        rate_mid = (rate_low + rate_high) / 2
        npv = funding_amount * -1
        for i in range(total_periods):
            npv += cashflow[i] / ((1 + rate_mid) ** (i + 1))

        if abs(npv) < tolerance:
            irr = rate_mid
            break

        if npv > 0:
            rate_low = rate_mid
        else:
            rate_high = rate_mid

    return irr

