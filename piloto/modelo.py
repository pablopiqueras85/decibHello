"""Modelo de la nota de ruido DecibHello (0-100, 100 = muy ruidoso), hora a hora.

Entrada: niveles del mapa estratégico de ruido (día, tarde, noche) y focos intermitentes cercanos.
El visor (visor_plantilla.html) tiene una copia en JavaScript de estas mismas funciones: si cambias una, cambia la otra.
"""

import math

# Franjas del mapa oficial: día 7-19 h, tarde 19-23 h, noche 23-7 h.
FRANJA = ["N"] * 7 + ["D"] * 12 + ["E"] * 4 + ["N"]
HORAS = {f: [h for h in range(24) if FRANJA[h] == f] for f in "DEN"}
# Pesos de cada franja en la nota global: la noche pesa más.
PESOS = {"D": 0.3, "E": 0.2, "N": 0.5}
# Nivel (dB) que da 50 puntos en cada franja. Es la misma penalización que el indicador europeo Lden
# (+5 dB tarde, +10 dB noche); de noche, 45 dB es la recomendación OMS para tráfico.
ANCLA_50 = {"D": 55, "E": 50, "N": 45}
PUNTOS_POR_DB = 50 / 30

# Forma típica del ruido de tráfico urbano a lo largo del día (dB relativos a la hora punta).
PERFIL_TRAFICO = [-6, -8, -9, -10, -10, -8, -4, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -2, -3, -4, -5]
# Forma del ruido de ocio nocturno dentro de la franja de noche (pico entre las 23 y la 1).
PERFIL_OCIO = {23: 0, 0: 0, 1: -1, 2: -3, 3: -6, 4: -9, 5: -12, 6: -15}
# Reparto horario de los focos intermitentes (bares, quejas, pisos turísticos): peso 1 = todo el extra en esa hora.
REPARTO_FOCOS = {19: 0.3, 20: 0.4, 21: 0.5, 22: 0.7, 23: 1, 0: 1, 1: 1, 2: 0.8, 3: 0.5, 4: 0.2}

# Día de la semana (0 = lunes ... 6 = domingo). Un "día" va de las 7:00 a las 7:00 del día siguiente: la noche del
# viernes (23-7 h) es la que empieza el viernes. Pesos en energía, normalizados a media 1 en la semana, para que la
# media de los 7 días siga siendo la del mapa oficial (media anual).
# SUPUESTOS v0, a calibrar con los datos por hora de los sensores municipales (tráfico y ocio).
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def _normalizar(pesos):
    media = sum(pesos) / len(pesos)
    return [p / media for p in pesos]


PESO_DIA_TRAFICO = {  # menos tráfico de día el fin de semana; más de noche el viernes y el sábado
    "D": _normalizar([1, 1, 1, 1, 1.05, 0.75, 0.55]),
    "E": _normalizar([1, 1, 1, 1.05, 1.1, 0.95, 0.8]),
    "N": _normalizar([0.85, 0.85, 0.9, 1.0, 1.25, 1.3, 0.8]),
}
PESO_DIA_OCIO_NOCHE = _normalizar([0.2, 0.25, 0.35, 0.7, 1.0, 1.0, 0.3])  # jueves ya fuerte; viernes y sábado, máximo
PESO_DIA_OCIO_TARDE = _normalizar([0.6, 0.6, 0.7, 0.85, 1.0, 1.0, 0.7])


def banda_a_db(texto):
    """'60 - 65 dB(A)' -> 62.5 ; '< 40 dB(A)' -> 37.5"""
    t = texto.replace("dB(A)", "").strip()
    if t.startswith("<"):
        return float(t[1:]) - 2.5
    lo, hi = (float(x) for x in t.split("-"))
    return (lo + hi) / 2


def energia(db):
    return 10 ** (db / 10)


def perfil_horario(total, trafico=None, ocio_noche=None, dia=None):
    """Reparte los niveles oficiales de día, tarde y noche en 24 horas (índice = hora del reloj).

    Dentro de cada franja, el tráfico sigue PERFIL_TRAFICO y el ocio nocturno PERFIL_OCIO; el resto del ruido
    se reparte plano. Se reescala para que la media energética de cada franja sea la del mapa oficial.
    Con `dia` (0-6), el tráfico y el ocio se multiplican por su peso de ese día; sin `dia`, es la media anual.
    Las horas 0-6 son la madrugada que sigue al día elegido.
    """
    db = [0.0] * 24
    for f, horas in HORAS.items():
        e_total = energia(total[f])
        traf = {h: 0.0 for h in horas}
        ocio = {h: 0.0 for h in horas}
        if trafico:
            forma = {h: energia(PERFIL_TRAFICO[h]) for h in horas}
            k = energia(trafico[f]) / (sum(forma.values()) / len(horas))
            traf = {h: forma[h] * k for h in horas}
        if ocio_noche is not None and f == "N":
            forma = {h: energia(PERFIL_OCIO[h]) for h in horas}
            k = energia(ocio_noche) / (sum(forma.values()) / len(horas))
            ocio = {h: forma[h] * k for h in horas}
        resto = max(0.0, e_total - (sum(traf.values()) + sum(ocio.values())) / len(horas))
        if not trafico:  # sin desglose (patio interior): todo con forma y pesos de tráfico
            forma = {h: energia(PERFIL_TRAFICO[h]) for h in horas}
            k = e_total / (sum(forma.values()) / len(horas))
            traf = {h: forma[h] * k for h in horas}
            resto = 0.0
        ajuste = e_total / (sum(traf[h] + ocio[h] + resto for h in horas) / len(horas))
        f_traf = PESO_DIA_TRAFICO[f][dia] if dia is not None else 1.0
        f_ocio = PESO_DIA_OCIO_NOCHE[dia] if dia is not None else 1.0
        # El resto del ruido (no atribuido a tráfico ni a ocio en el mapa) varía como la mezcla de ambos en esa franja.
        e_traf, e_ocio = sum(traf.values()), sum(ocio.values())
        f_resto = (e_traf * f_traf + e_ocio * f_ocio) / (e_traf + e_ocio) if e_traf + e_ocio else f_traf
        for h in horas:
            db[h] = 10 * math.log10((traf[h] * f_traf + ocio[h] * f_ocio + resto * f_resto) * ajuste)
    # Suaviza el salto entre franjas (18-19 h, 22-23 h) conservando la energía de cada pareja de horas.
    # Las 6 y las 7 no se mezclan: en un día de 7:00 a 7:00 pertenecen a mañanas distintas.
    for h1, h2 in ((18, 19), (22, 23)):
        e1, e2 = energia(db[h1]), energia(db[h2])
        db[h1], db[h2] = 10 * math.log10((2 * e1 + e2) / 3), 10 * math.log10((e1 + 2 * e2) / 3)
    return db


def suavizar_extremos(v):
    """Comprime suavemente por encima de 70 y por debajo de 30 para no saturar en 0 o 100 y mantener el orden."""
    if v > 70:
        return 70 + 30 * (1 - math.exp(-(v - 70) / 30))
    if v < 30:
        return 30 - 30 * (1 - math.exp(-(30 - v) / 30))
    return v


def peso_focos(h, dia):
    """Peso de los focos intermitentes en la hora h: reparto horario y, si hay día, su peso semanal."""
    peso = REPARTO_FOCOS.get(h, 0)
    if dia is not None and peso:
        peso *= PESO_DIA_OCIO_TARDE[dia] if FRANJA[h] == "E" else PESO_DIA_OCIO_NOCHE[dia]
    return peso


def notas_horarias(db, extra, dia=None):
    """Nota 0-100 de cada hora: nivel respecto al umbral de su franja + focos intermitentes repartidos por hora."""
    return [suavizar_extremos(50 + (db[h] - ANCLA_50[FRANJA[h]]) * PUNTOS_POR_DB + extra * peso_focos(h, dia)) for h in range(24)]


def resumen(notas):
    franjas = {f: sum(notas[h] for h in HORAS[f]) / len(HORAS[f]) for f in "DEN"}
    return franjas, sum(PESOS[f] * franjas[f] for f in "DEN")


def extra_focos(ocio, bares, quejas, turisticos):
    """Puntos extra por focos intermitentes a menos de 100 m (máximo 25, en las horas punta del ocio)."""
    return min(10, 4 * ocio) + min(6, 1.2 * math.sqrt(bares)) + min(6, 2 * math.sqrt(quejas)) + min(3, math.sqrt(turisticos) / 3)


def calcular(mapa, focos=None, dia=None):
    """mapa: {'TOTAL_D':banda,...,'TRANSIT_N':banda,'OCI_N':banda} (texto de banda o dB); dia: 0-6 o None (media anual)."""
    db_de = lambda v: v if isinstance(v, (int, float)) else banda_a_db(v)
    total = {f: db_de(mapa[f"TOTAL_{f}"]) for f in "DEN"}
    trafico = {f: db_de(mapa[f"TRANSIT_{f}"]) for f in "DEN"} if "TRANSIT_D" in mapa else None
    ocio = db_de(mapa["OCI_N"]) if "OCI_N" in mapa else None
    db = perfil_horario(total, trafico, ocio, dia)
    notas = notas_horarias(db, extra_focos(**focos) if focos else 0, dia)
    franjas, global_ = resumen(notas)
    return {"db": db, "notas": notas, "franjas": franjas, "global": global_}


def aviso_picos(ancho_m, quejas_recogida):
    """Aviso de picos nocturnos (camiones de recogida y limpieza). No entra en la nota 0-100.

    ancho_m: anchura de la calle entre portales de lados opuestos (-1 si no se sabe).
    quejas_recogida: quejas por ruido de limpieza y recogida (IRIS 2023-2026) a menos de 100 m.
    """
    estrecha = 0 <= ancho_m < 12
    if (estrecha and quejas_recogida >= 1) or quejas_recogida >= 5:
        nivel = "alto"
    elif estrecha or quejas_recogida >= 1:
        nivel = "medio"
    else:
        nivel = "bajo"
    return nivel
