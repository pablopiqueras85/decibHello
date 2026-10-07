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
# Escala de cada franja: nivel (dB) que da 0 puntos y nivel que da 100. Son los extremos reales de Barcelona:
# 0 = calle muy tranquila; 100 = como Tuset un viernes de madrugada (~70 dB de noche). Lineal entre ambos.
# La noche tiene los dos extremos más bajos: el mismo ruido puntúa más de noche.
ESCALA = {"D": (45, 75), "E": (45, 75), "N": (35, 70)}

# Formas horarias y pesos por día de la semana MEDIDOS con la red municipal de sensores (2023, datos por hora):
# ver sensores.py -> perfiles_sensores.json. Si ese fichero no existe, se usan los supuestos iniciales (v0).
import json as _json
from pathlib import Path as _Path

DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def _normalizar(pesos):
    media = sum(pesos) / len(pesos)
    return [p / media for p in pesos]


_F = _Path(__file__).with_name("perfiles_sensores.json")
PERFILES = _json.loads(_F.read_text(encoding="utf-8")) if _F.exists() else None
if PERFILES:
    PERFIL_TRAFICO = PERFILES["trafico"]["forma_horaria_db"]
    _ocio = PERFILES["ocio"]["forma_horaria_db"]
    _max_noche = max(_ocio[h] for h in (23, 0, 1, 2, 3, 4, 5, 6))
    PERFIL_OCIO = {h: round(_ocio[h] - _max_noche, 1) for h in (23, 0, 1, 2, 3, 4, 5, 6)}
    PESO_DIA_TRAFICO = {f: _normalizar(PERFILES["trafico"]["pesos_dia"][f]) for f in "DEN"}
    PESO_DIA_OCIO_NOCHE = _normalizar(PERFILES["ocio"]["pesos_dia"]["N"])
    PESO_DIA_OCIO_TARDE = _normalizar(PERFILES["ocio"]["pesos_dia"]["E"])
    # Pesos por día y hora (más finos: el domingo por la mañana baja más que el domingo por la tarde).
    PESO_DIA_HORA_TRAFICO = PERFILES["trafico"].get("pesos_dia_hora")
    PESO_DIA_HORA_OCIO = PERFILES["ocio"].get("pesos_dia_hora")
else:  # supuestos v0
    PERFIL_TRAFICO = [-6, -8, -9, -10, -10, -8, -4, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -2, -3, -4, -5]
    PERFIL_OCIO = {23: 0, 0: 0, 1: -1, 2: -3, 3: -6, 4: -9, 5: -12, 6: -15}
    PESO_DIA_TRAFICO = {"D": _normalizar([1, 1, 1, 1, 1.05, 0.75, 0.55]), "E": _normalizar([1, 1, 1, 1.05, 1.1, 0.95, 0.8]),
                        "N": _normalizar([0.85, 0.85, 0.9, 1.0, 1.25, 1.3, 0.8])}
    PESO_DIA_OCIO_NOCHE = _normalizar([0.2, 0.25, 0.35, 0.7, 1.0, 1.0, 0.3])
    PESO_DIA_OCIO_TARDE = _normalizar([0.6, 0.6, 0.7, 0.85, 1.0, 1.0, 0.7])
    PESO_DIA_HORA_TRAFICO = PESO_DIA_HORA_OCIO = None
# Horarios de los locales de noche (discotecas, bares musicales, coctelerías): las noches en que hay más locales
# abiertos de madrugada a menos de 150 m son más ruidosas. Coeficiente ajustado con los sensores (horarios_ocio.py):
# dB extra por unidad de log(1 + carga de esa noche), respecto a la media de la semana del propio tramo.
K_HORARIOS = 2.79
# Bares y discotecas suman ruido de forma proporcional (validado con sensores por distritos, ver ocio_oculto.md):
# dB por unidad de log(1 + número a menos de 100 m), por franja. Sin locales, cero. Ajuste no negativo y sin término
# fijo, para no subir calles sin locales. Los pisos turísticos no suben la media horaria (coeficiente 0 en los
# sensores): cuentan en el aviso de picos nocturnos.
COEF_LOCALES = {"D": {"bares": 1.32, "musicales": 1.68}, "E": {"bares": 2.90, "musicales": 0.72}, "N": {"bares": 1.93, "musicales": 0.0}}


# Obra pública activa a menos de 25 m del portal: +2 dB de 8 a 18 h, de lunes a viernes, mientras dure
# (validado con sensores, ver obras_validacion.md). Es temporal: desaparece cuando la obra termina.
OBRA_DB = 2.0
HORAS_OBRA = range(8, 18)


def suma_obra(db, dia):
    """Suma el ruido de una obra activa al perfil horario (en el sitio). Sin día: media de la semana (5 de 7 días)."""
    extra = OBRA_DB if dia is not None else 10 * math.log10((5 * 10 ** (OBRA_DB / 10) + 2) / 7)
    if dia is None or dia < 5:
        for h in HORAS_OBRA:
            db[h] += extra


# Planta del piso. ESTIMACIÓN a partir de estudios de ruido en calles; aún sin medir en Barcelona.
# El mapa oficial calcula el ruido a 4 m de altura (más o menos un 1.º). En calles estrechas entre edificios altos el
# sonido rebota y casi no baja con la altura; en calles anchas baja de forma progresiva. El ático retirado de la
# fachada gana la pantalla del pretil y los bajos están pegados al tráfico y a la gente.
PLANTA_ALTURA_M = 3.0      # altura de cada planta
PLANTA_BAJA_DB = 1.0       # bajos y entresuelos
ATICO_DB = -3.0            # ático retirado de la fachada
PLANTA_MAX_DB = 8.0        # como mucho, 8 dB menos que en el 1.º


def correccion_planta(planta, plantas_edificio=-1, ancho_m=-1):
    """dB que se suman a la fachada a la calle según la planta.

    planta: 0 = bajo o entresuelo, 1, 2, 3... = número de planta, "atico" = ático. None o 1 = sin corrección.
    plantas_edificio: plantas sobre rasante del edificio (Catastro), -1 si no se sabe.
    ancho_m: anchura de la calle entre fachadas, -1 si no se sabe.
    """
    if planta is None or planta == 1:
        return 0.0
    if planta == 0:
        return PLANTA_BAJA_DB
    alto = PLANTA_ALTURA_M * plantas_edificio + 1 if plantas_edificio > 0 else 20.0
    ancho = ancho_m if ancho_m >= 3 else 20.0
    pendiente = 0.4 * (1 - min(alto / ancho, 1.0))   # dB por metro: 0 en calle estrecha y alta, 0,4 en calle muy abierta
    extra = 0.0
    if planta == "atico":
        planta, extra = (plantas_edificio if plantas_edificio > 1 else 7), ATICO_DB
    altura = 4 + PLANTA_ALTURA_M * (planta - 1)
    return -min(PLANTA_MAX_DB, pendiente * max(0.0, altura - 4)) + extra


def correccion_locales(bares, musicales):
    """dB a sumar por franja según bares y bares musicales/discotecas a menos de 100 m."""
    return {f: c["bares"] * math.log1p(bares) + c["musicales"] * math.log1p(musicales) for f, c in COEF_LOCALES.items()}
# Un "día" va de las 7:00 a las 7:00 del día siguiente: la noche del viernes (23-7 h) es la que empieza el viernes.


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
    sigue la forma de ambos. Se reescala para que la media energética de cada franja sea la del mapa oficial.
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
        # El resto (ruido sin fuente asignada en el mapa) sigue la forma horaria de tráfico + ocio de la franja,
        # no un reparto plano: de madrugada baja como baja la actividad de la calle.
        base = {h: traf[h] + ocio[h] for h in horas}
        media_base = sum(base.values()) / len(horas)
        forma_resto = {h: (base[h] / media_base if media_base else 1.0) for h in horas}
        for h in horas:
            ft, fo, fr = f_traf, f_ocio, f_resto
            if dia is not None and PESO_DIA_HORA_TRAFICO:
                ft, fo = PESO_DIA_HORA_TRAFICO[dia][h], PESO_DIA_HORA_OCIO[dia][h]
                fr = (traf[h] * ft + ocio[h] * fo) / (traf[h] + ocio[h]) if traf[h] + ocio[h] else ft
            db[h] = 10 * math.log10((traf[h] * ft + ocio[h] * fo + resto * forma_resto[h] * fr) * ajuste)
    # Suaviza el salto entre franjas (18-19 h, 22-23 h) conservando la energía de cada pareja de horas.
    # Las 6 y las 7 no se mezclan: en un día de 7:00 a 7:00 pertenecen a mañanas distintas.
    for h1, h2 in ((18, 19), (22, 23)):
        e1, e2 = energia(db[h1]), energia(db[h2])
        db[h1], db[h2] = 10 * math.log10((2 * e1 + e2) / 3), 10 * math.log10((e1 + 2 * e2) / 3)
    return db


def nota_db(db, franja):
    """Nota 0-100 de un nivel en dB dentro de su franja (lineal entre los extremos de ESCALA)."""
    cero, cien = ESCALA[franja]
    return min(100.0, max(0.0, (db - cero) / (cien - cero) * 100))


def notas_horarias(db, dia=None):
    """Nota 0-100 de cada hora a partir de su nivel en dB: la MISMA fórmula para todo (medido o estimado)."""
    return [nota_db(db[h], FRANJA[h]) for h in range(24)]


def resumen(notas):
    franjas = {f: sum(notas[h] for h in HORAS[f]) / len(HORAS[f]) for f in "DEN"}
    return franjas, sum(PESOS[f] * franjas[f] for f in "DEN")


def perfil_medido(db_dias, dia=None):
    """Nivel por hora medido por un sensor: db_dias[dia][hora]. Sin día: media energética de los 7 días."""
    if dia is not None:
        return list(db_dias[dia])
    return [10 * math.log10(sum(energia(db_dias[d][h]) for d in range(7)) / 7) for h in range(24)]


def ajuste_noches(carga):
    """dB a sumar a cada noche (lunes..domingo) según los locales abiertos de madrugada; media energética 0 en la semana."""
    lc = [math.log1p(c) for c in carga]
    media = sum(lc) / 7
    g = [10 ** (K_HORARIOS * (v - media) / 10) for v in lc]
    mg = sum(g) / 7
    return [round(10 * math.log10(x / mg), 1) for x in g]


def calcular(mapa, focos=None, dia=None, medido=None, locales=None, ajuste_noche=None, obra=False, planta_db=0.0):
    # focos: se mantiene por compatibilidad; ya no suma puntos. Todo pasa por los dB (validado con sensores).
    """mapa: {'TOTAL_D':banda,...,'TRANSIT_N':banda,'OCI_N':banda} (texto de banda o dB); dia: 0-6 o None (media anual).
    medido: perfil de un sensor municipal cercano (7 x 24 dB). Si se da, sustituye al mapa y no se suman focos,
    porque la medición ya los incluye."""
    if medido is not None:
        db = [v + planta_db for v in perfil_medido(medido, dia)]
        if obra:
            suma_obra(db, dia)
        notas = notas_horarias(db, dia)
        franjas, global_ = resumen(notas)
        return {"db": db, "notas": notas, "franjas": franjas, "global": global_}
    db_de = lambda v: v if isinstance(v, (int, float)) else banda_a_db(v)
    corr = correccion_locales(*locales) if locales else {f: 0.0 for f in "DEN"}
    total = {f: db_de(mapa[f"TOTAL_{f}"]) + corr[f] for f in "DEN"}
    trafico = {f: db_de(mapa[f"TRANSIT_{f}"]) for f in "DEN"} if "TRANSIT_D" in mapa else None
    ocio = db_de(mapa["OCI_N"]) if "OCI_N" in mapa else None
    db = perfil_horario(total, trafico, ocio, dia)
    if ajuste_noche is not None and dia is not None:
        for h in HORAS["N"]:
            db[h] += ajuste_noche[dia]
    db = [v + planta_db for v in db]
    if obra:
        suma_obra(db, dia)
    notas = notas_horarias(db, dia)
    franjas, global_ = resumen(notas)
    return {"db": db, "notas": notas, "franjas": franjas, "global": global_}


def aviso_picos(ancho_m, quejas_recogida, turisticos=0):
    """Aviso de picos nocturnos (camiones de recogida y limpieza). No entra en la nota 0-100.

    ancho_m: anchura de la calle entre portales de lados opuestos (-1 si no se sabe).
    quejas_recogida: quejas por ruido de limpieza y recogida (IRIS 2023-2026) a menos de 100 m.
    """
    estrecha = 0 <= ancho_m < 12
    # Pisos turísticos: llegadas y salidas a deshoras (maletas, grupos); 20 o más a menos de 100 m cuentan como foco.
    turistico = turisticos >= 20
    if (estrecha and (quejas_recogida >= 1 or turistico)) or quejas_recogida >= 5 or (turistico and quejas_recogida >= 1):
        nivel = "alto"
    elif estrecha or quejas_recogida >= 1 or turistico:
        nivel = "medio"
    else:
        nivel = "bajo"
    return nivel
