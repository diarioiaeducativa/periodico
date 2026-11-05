#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Música propia para los vídeos del diario, compuesta por programa, sin licencias de terceros
(ADR 0016). Electrónica con la estructura del vídeo: entrada, una sección por noticia con una
subida y un golpe en cada corte, y cierre. Cada vídeo lleva un estilo distinto: tempo,
tonalidad, modo, progresión de acordes, patrón de batería, timbre y arpegio.

    musica.py SALIDA.wav COMPASES_INTRO NOTICIAS COMPASES_NOTICIA COMPASES_CIERRE [ESTILO_JSON]

Sin ESTILO_JSON, el del primer vídeo (120 ppm, la menor, i–VI–III–VII, bombo a negras, sierra).
`elegir(usados, semilla)` da un estilo que no esté en la lista de usados. Solo numpy.
"""
import json
import random
import sys
import wave

import numpy as np

SR = 44100

TEMPOS = [100, 106, 112, 116, 120, 124, 128]
TONICAS = {"do": 48, "re": 50, "mi": 52, "fa": 53, "sol": 55, "la": 57, "si♭": 58}
# Grados (0 = tónica) de cada acorde de la progresión; uno por compás
PROGRESIONES = {
    "menor": {"i-VI-III-VII": [0, 5, 2, 6], "i-iv-VI-V": [0, 3, 5, 4], "i-VII-VI-VII": [0, 6, 5, 6], "VI-VII-i-i": [5, 6, 0, 0]},
    "mayor": {"I-V-vi-IV": [0, 4, 5, 3], "I-vi-IV-V": [0, 5, 3, 4], "IV-I-V-vi": [3, 0, 4, 5], "I-IV-vi-V": [0, 3, 5, 4]},
}
ESCALAS = {"menor": [0, 2, 3, 5, 7, 8, 10], "mayor": [0, 2, 4, 5, 7, 9, 11]}
BATERIAS = ["negras", "quebrada", "media"]
TIMBRES = ["sierra", "cuadrada", "suave"]
PRIMERO = {"tempo": 120, "tonica": "la", "modo": "menor", "progresion": "i-VI-III-VII", "bateria": "negras",
           "timbre": "sierra", "arpegio": False}


def clave(estilo):
    """Lo que no puede repetirse: la combinación de tempo, tonalidad, modo y progresión."""
    return f'{estilo["tempo"]}|{estilo["tonica"]}|{estilo["modo"]}|{estilo["progresion"]}'


def elegir(usados, semilla):
    """Un estilo nuevo: distinta combinación que todos los usados y, si se puede, también distinto
    tempo, tonalidad y batería que el último."""
    r = random.Random(semilla)
    vistos = {clave(u) for u in usados}
    ultimo = usados[-1] if usados else PRIMERO
    for _ in range(500):
        modo = r.choice(list(PROGRESIONES))
        e = {"tempo": r.choice(TEMPOS), "tonica": r.choice(list(TONICAS)), "modo": modo,
             "progresion": r.choice(list(PROGRESIONES[modo])), "bateria": r.choice(BATERIAS),
             "timbre": r.choice(TIMBRES), "arpegio": r.random() < 0.6, "semilla": r.randrange(10**6)}
        if clave(e) in vistos:
            continue
        if any(e[k] == ultimo.get(k) for k in ("tempo", "tonica", "bateria")) and _ < 400:
            continue
        return e
    raise RuntimeError("no queda ningún estilo sin usar")


def compas_seg(estilo):
    return 4 * 60 / estilo["tempo"]


class Sintetizador:
    def __init__(self, estilo):
        self.e = estilo
        self.rng = np.random.default_rng(estilo.get("semilla", 7))
        self.pulso = 60 / estilo["tempo"]

    def t(self, n):
        return np.arange(int(n * SR)) / SR

    def filtro(self, x, bajo=None, alto=None):
        f = np.fft.rfftfreq(len(x), 1 / SR)
        g = np.ones_like(f)
        if bajo:
            g *= 1 / (1 + (f / bajo) ** 4)
        if alto:
            g *= 1 - 1 / (1 + (f / alto) ** 4)
        return np.fft.irfft(np.fft.rfft(x) * g, len(x))

    def bombo(self):
        tt = self.t(0.45)
        s = np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-tt * 28)) / SR) * np.exp(-tt * 7)
        s[:200] += np.linspace(0.6, 0, 200) * self.rng.standard_normal(200) * 0.4
        return np.tanh(s * 1.6)

    def caja(self):
        tt = self.t(0.3)
        ruido = self.filtro(self.rng.standard_normal(len(tt)), bajo=5000, alto=1200) * np.exp(-tt * 18)
        tono = np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 25) * 0.5
        return (ruido + tono) * 0.8

    def palmas(self):
        s = np.zeros(int(0.35 * SR))
        for k, d in enumerate((0, 0.011, 0.023)):
            n = self.rng.standard_normal(int(0.3 * SR)) * np.exp(-self.t(0.3) * (40 if k < 2 else 14))
            i = int(d * SR)
            s[i:i + len(n)] += n[:len(s) - i]
        return self.filtro(s, bajo=2600, alto=900) * 0.9

    def charles(self, abierto=False):
        d = 0.22 if abierto else 0.05
        n = self.rng.standard_normal(int(d * SR)) * np.exp(-self.t(d) * (14 if abierto else 70))
        return self.filtro(n, alto=7000) * (0.35 if abierto else 0.28)

    def onda(self, frec, dur, desafin=(0,)):
        tt = self.t(dur)
        timbre = self.e.get("timbre", "sierra")
        salida = 0
        for c in desafin:
            fase = (tt * frec * 2 ** (c / 1200)) % 1
            if timbre == "cuadrada":
                salida = salida + np.where(fase < 0.5, 1.0, -1.0) * 0.8
            elif timbre == "suave":
                salida = salida + np.sin(2 * np.pi * fase) + 0.3 * np.sin(4 * np.pi * fase)
            else:
                salida = salida + 2 * fase - 1
        return salida / len(desafin)

    @staticmethod
    def nota(m):
        return 440 * 2 ** ((m - 69) / 12)

    def bajo_nota(self, m, dur):
        s = self.onda(self.nota(m), dur, (0, 7))
        env = np.minimum(1, self.t(dur) * 200) * np.exp(-self.t(dur) * 5)
        return self.filtro(s * env, bajo=420) * 0.55

    def acorde(self, notas, dur, brillo=1800, pad=False):
        s = sum(self.onda(self.nota(m), dur, (-9, 0, 9)) for m in notas) / len(notas)
        tt = self.t(dur)
        env = np.minimum(1, tt * (6 if pad else 120)) * (np.ones_like(tt) if pad else np.exp(-tt * 9))
        env *= np.minimum(1, (dur - tt) * 30)
        return self.filtro(s * env, bajo=brillo) * (0.22 if pad else 0.3)

    def pluck(self, m, dur):
        tt = self.t(dur)
        s = self.onda(self.nota(m), dur) * np.exp(-tt * 14) * np.minimum(1, tt * 400)
        return self.filtro(s, bajo=3500) * 0.22

    def subida(self, dur):
        n = self.rng.standard_normal(int(dur * SR))
        trozos = np.array_split(n, 16)
        salida = np.concatenate([self.filtro(c, bajo=600 + 9000 * (k / 15) ** 2) for k, c in enumerate(trozos)])
        return salida * np.linspace(0, 1, len(salida)) ** 2 * 0.35

    def golpe(self):
        tt = self.t(1.2)
        s = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-tt * 12)) / SR) * np.exp(-tt * 3.5)
        s += self.filtro(self.rng.standard_normal(len(tt)), bajo=3000) * np.exp(-tt * 9) * 0.5
        return np.tanh(s * 1.3) * 0.7


def acordes(estilo):
    """Las cuatro tríadas (con la octava) de la progresión y sus fundamentales para el bajo."""
    esc = ESCALAS[estilo["modo"]]
    base = TONICAS[estilo["tonica"]]
    grados = PROGRESIONES[estilo["modo"]][estilo["progresion"]]
    salida, raices = [], []
    for g in grados:
        notas = [base + esc[(g + k) % 7] + 12 * ((g + k) // 7) for k in (0, 2, 4)]
        salida.append(tuple(notas + [notas[0] + 12]))
        raices.append(notas[0] - 12 if notas[0] - 12 >= 36 else notas[0])
    return salida, raices


def poner(pista, sonido, seg, vol=1.0):
    i = int(seg * SR)
    if i >= len(pista) or i < 0:
        return
    fin = min(len(pista), i + len(sonido))
    pista[i:fin] += sonido[:fin - i] * vol


def componer(salida, c_intro, noticias, c_not, c_cierre, estilo=None):
    estilo = estilo or PRIMERO
    s = Sintetizador(estilo)
    P = s.pulso
    C = 4 * P
    compases = c_intro + noticias * c_not + c_cierre
    total = compases * C + 1.5
    bat = np.zeros(int(total * SR))
    mus = np.zeros_like(bat)
    efe = np.zeros_like(bat)
    lado = np.ones_like(bat)
    prog, raices = acordes(estilo)
    k_bombo, k_palmas, k_caja = s.bombo(), s.palmas(), s.caja()
    env_lado = 1 - 0.75 * np.exp(-s.t(P) * 9)
    patron = estilo.get("bateria", "negras")

    def bombeo(seg):
        i = int(seg * SR)
        n = min(len(env_lado), len(lado) - i)
        if n > 0:
            lado[i:i + n] = np.minimum(lado[i:i + n], env_lado[:n])

    for c in range(compases):
        ini = c * C
        ac = prog[c % 4]
        if c < c_intro:
            poner(mus, s.acorde(ac, C, brillo=500 + 900 * c, pad=True), ini, 3.0)
            for p in range(8):
                poner(bat, s.charles(), ini + p * P / 2, 1.2 + 0.6 * (p % 2))
        elif c < c_intro + noticias * c_not:
            if patron == "negras":
                golpes_bombo, golpes_caja = [0, 1, 2, 3], []
            elif patron == "quebrada":
                golpes_bombo, golpes_caja = [0, 1.5, 2.5], [1, 3]
            else:   # media: a medio tiempo
                golpes_bombo, golpes_caja = [0, 2.75], [2]
            for b in golpes_bombo:
                poner(bat, k_bombo, ini + b * P, 0.95)
                bombeo(ini + b * P)
            for b in golpes_caja:
                poner(bat, k_caja, ini + b * P, 0.7)
            for p in range(4):
                poner(bat, s.charles(abierto=True), ini + p * P + P / 2, 0.7)
                for q in range(4):
                    poner(bat, s.charles(), ini + p * P + q * P / 4, 0.5 if q % 2 else 0.25)
                if patron == "negras" and p in (1, 3):
                    poner(bat, k_palmas, ini + p * P, 0.8)
                m = raices[c % 4] + (12 if p == 3 else 0)
                poner(mus, s.bajo_nota(m, P / 2 * 0.9), ini + p * P + P / 2)
            for g in (0.75, 1.5, 2.5, 3.25):
                poner(mus, s.acorde(ac, P * 0.45, brillo=2600), ini + g * P, 0.9)
            poner(mus, s.acorde(ac, C, brillo=900, pad=True), ini, 0.5)
            if estilo.get("arpegio"):
                orden = [0, 1, 2, 3, 2, 1, 0, 2]
                for k in range(8):
                    poner(mus, s.pluck(ac[orden[k]] + 12, P / 2), ini + k * P / 2, 0.9)
        else:
            poner(mus, s.acorde(ac, C * (2 if c == compases - 1 else 1), brillo=1400, pad=True), ini, 2.6)
            if c == c_intro + noticias * c_not:
                poner(bat, k_bombo, ini, 1.0)
    cortes = [c_intro + k * c_not for k in range(noticias + 1)]
    for c in cortes:
        seg = c * C
        poner(efe, s.subida(P * 2), seg - P * 2)
        poner(efe, s.golpe(), seg, 0.8 if c in (c_intro, cortes[-1]) else 0.45)
    mezcla = bat * 0.9 + mus * lado * 1.1 + efe
    mezcla = np.tanh(mezcla * 1.2)
    mezcla *= np.minimum(1, (total - np.arange(len(mezcla)) / SR) / 1.5)
    mezcla = mezcla / np.max(np.abs(mezcla)) * 0.89
    der = mezcla.copy()
    der[220:] = 0.85 * mezcla[220:] + 0.15 * mezcla[:-220]
    estereo = np.stack([mezcla, der], axis=1)
    with wave.open(str(salida), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((estereo * 32767).astype("<i2").tobytes())
    return total


def main():
    salida = sys.argv[1]
    c_intro, noticias, c_not, c_cierre = (int(x) for x in sys.argv[2:6])
    estilo = json.loads(sys.argv[6]) if len(sys.argv) > 6 else None
    total = componer(salida, c_intro, noticias, c_not, c_cierre, estilo)
    print(f"música: {total:.1f} s")


if __name__ == "__main__":
    main()
