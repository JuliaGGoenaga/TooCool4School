#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_imagenes.py — Genera una ilustración SVG por estrategia en assets/img/.

Son ilustraciones planas y ligeras, coloreadas según el grupo (A/B/C/D).
Puedes sustituir cualquiera por una foto real: guarda tu imagen en
assets/img/ y actualiza el campo "imagen" de la ficha correspondiente.
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "img")
os.makedirs(OUT, exist_ok=True)

# Paleta por grupo: (principal, oscuro, cielo claro, suelo)
PAL = {
    "A": ("#1f8f6f", "#146b52", "#e8f4ee", "#d3e9dd"),
    "B": ("#2b6cb0", "#1f5290", "#e7f0fa", "#d3e3f4"),
    "C": ("#b7791f", "#8f5e14", "#f8efda", "#f0e0bd"),
    "D": ("#a04668", "#7d3450", "#f7e8ee", "#efd4de"),
}
SUN = "#f4b740"
GLASS = "#cfe6f2"


def frame(g, inner):
    p, d, sky, ground = PAL[g]
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" fill="none">'
        '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{sky}"/><stop offset="1" stop-color="#ffffff"/>'
        '</linearGradient></defs>'
        '<rect width="480" height="300" fill="url(#sky)"/>'
        + inner.format(p=p, d=d, sky=sky, ground=ground, sun=SUN, glass=GLASS)
        + '</svg>'
    )


def sun(cx=402, cy=64, r=30, rays=True):
    s = ''
    if rays:
        import math
        for i in range(12):
            a = math.radians(i * 30)
            x1 = cx + math.cos(a) * (r + 8); y1 = cy + math.sin(a) * (r + 8)
            x2 = cx + math.cos(a) * (r + 20); y2 = cy + math.sin(a) * (r + 20)
            s += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{SUN}" stroke-width="5" stroke-linecap="round" opacity=".85"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUN}"/>'
    return s


def ground(y=232):
    return f'<rect x="0" y="{y}" width="480" height="{300-y}" fill="{{ground}}"/>'


def tree(cx, base, s=1.0, trunk="#9c6b3f"):
    h = 70 * s
    return (
        f'<rect x="{cx-5}" y="{base-h*0.35:.0f}" width="10" height="{h*0.35:.0f}" rx="4" fill="{trunk}"/>'
        f'<circle cx="{cx}" cy="{base-h*0.55:.0f}" r="{28*s:.0f}" fill="{{p}}"/>'
        f'<circle cx="{cx-20*s:.0f}" cy="{base-h*0.4:.0f}" r="{20*s:.0f}" fill="{{d}}"/>'
        f'<circle cx="{cx+20*s:.0f}" cy="{base-h*0.42:.0f}" r="{20*s:.0f}" fill="{{d}}"/>'
    )


# Motivo específico por código de estrategia -------------------------------
M = {}

# ---- A. Pasiva exterior ----
M["A.1"] = sun(410, 60) + ground() + (
    # velas de sombra tensadas
    '<path d="M60 120 L250 90 L235 150 L70 165 Z" fill="{p}" opacity=".9"/>'
    '<path d="M270 96 L430 130 L410 175 L255 152 Z" fill="{d}" opacity=".9"/>'
    '<line x1="66" y1="120" x2="70" y2="232" stroke="{d}" stroke-width="6"/>'
    '<line x1="248" y1="92" x2="250" y2="232" stroke="{d}" stroke-width="6"/>'
    '<line x1="428" y1="128" x2="430" y2="232" stroke="{d}" stroke-width="6"/>'
    '<ellipse cx="250" cy="250" rx="150" ry="12" fill="{d}" opacity=".18"/>'
)

M["A.2"] = sun(60, 60) + ground() + (
    tree(150, 232, 1.3) + tree(300, 232, 1.05) + tree(400, 232, 0.85)
    + '<rect x="0" y="256" width="480" height="6" fill="{d}" opacity=".25"/>'
)

# despiece de pavimento (aparejo a matajunta), sin más elementos
_pav_rows = ''
for _r in range(6):
    _y = 60 + _r * 32
    _off = 0 if _r % 2 == 0 else -42
    for _c in range(-1, 7):
        _x = 44 + _off + _c * 84
        _fill = "{ground}" if (_r + _c) % 3 == 0 else "#ffffff"
        _pav_rows += f'<rect x="{_x}" y="{_y}" width="78" height="28" rx="4" fill="{_fill}" stroke="{{p}}" stroke-width="2.5"/>'
M["A.3.1"] = (
    '<defs><clipPath id="pv"><rect x="42" y="58" width="396" height="188" rx="14"/></clipPath></defs>'
    '<rect x="42" y="58" width="396" height="188" rx="14" fill="{ground}"/>'
    '<g clip-path="url(#pv)">' + _pav_rows + '</g>'
    '<rect x="42" y="58" width="396" height="188" rx="14" fill="none" stroke="{d}" stroke-width="3"/>'
)

M["A.3.2"] = ground() + sun(240, 70) + (
    # superficie clara reflejando rayos
    '<rect x="60" y="210" width="360" height="26" rx="6" fill="#ffffff" stroke="{d}" stroke-width="2"/>'
    '<line x1="240" y1="100" x2="150" y2="205" stroke="{sun}" stroke-width="5" stroke-linecap="round"/>'
    '<line x1="240" y1="100" x2="330" y2="205" stroke="{sun}" stroke-width="5" stroke-linecap="round"/>'
    '<line x1="150" y1="205" x2="120" y2="150" stroke="{sun}" stroke-width="4" stroke-dasharray="3 6" stroke-linecap="round"/>'
    '<line x1="330" y1="205" x2="360" y2="150" stroke="{sun}" stroke-width="4" stroke-dasharray="3 6" stroke-linecap="round"/>'
)

M["A.4"] = sun(410, 58) + ground() + (
    tree(188, 232, 1.05)
    # pérgola con banco y fuente
    + '<rect x="230" y="120" width="150" height="8" rx="3" fill="{d}"/>'
    '<line x1="240" y1="124" x2="240" y2="232" stroke="{d}" stroke-width="7"/>'
    '<line x1="370" y1="124" x2="370" y2="232" stroke="{d}" stroke-width="7"/>'
    + ''.join(f'<line x1="{245+i*22}" y1="120" x2="{245+i*22}" y2="108" stroke="{{p}}" stroke-width="5"/>' for i in range(6))
    + '<rect x="255" y="195" width="90" height="12" rx="4" fill="{p}"/>'
    '<rect x="262" y="207" width="8" height="25" fill="{d}"/><rect x="330" y="207" width="8" height="25" fill="{d}"/>'
    '<circle cx="150" cy="248" r="10" fill="{glass}"/>'
)

# pavimento drenante: losetas con juntas permeables y gotas grandes infiltrando
_drp = ''
for _i in range(6):
    _x = 80 + _i * 60
    _y = 44 + (28 if _i % 2 else 0)
    _drp += f'<path d="M{_x} {_y} q11 20 0 34 a17 17 0 1 1 0 -34z" fill="{{glass}}" stroke="{{p}}" stroke-width="2"/>'
    _drp += f'<circle cx="{_x}" cy="{_y+22}" r="4" fill="#ffffff" opacity=".7"/>'
M["A.5.1"] = (
    '<rect x="40" y="150" width="400" height="96" rx="10" fill="{ground}"/>'
    + ''.join(
        f'<rect x="{48+ (_i%5)*80}" y="{162+ (_i//5)*40}" width="72" height="32" rx="5" fill="#ffffff" stroke="{{d}}" stroke-width="2"/>'
        for _i in range(10))
    # juntas permeables verticales
    + ''.join(f'<rect x="{120+_j*80}" y="150" width="8" height="96" fill="{{p}}" opacity=".85"/>' for _j in range(4))
    # flechas de infiltración por las juntas
    + ''.join(f'<path d="M{124+_j*80} 200 v30" stroke="{{glass}}" stroke-width="4" stroke-linecap="round"/><path d="M{118+_j*80} 224 l6 8 l6 -8" fill="none" stroke="{{glass}}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>' for _j in range(4))
    + _drp
)

M["A.5.2"] = ground() + sun(410, 56) + (
    # depósito de agua con nivel, grifo, canalón de recogida y gota
    '<rect x="150" y="96" width="150" height="136" rx="16" fill="#ffffff" stroke="{d}" stroke-width="3"/>'
    # agua dentro (nivel)
    '<path d="M156 150 h138 v72 a10 10 0 0 1 -10 10 h-118 a10 10 0 0 1 -10 -10 z" fill="{glass}"/>'
    '<path d="M156 150 q34 -12 69 0 t69 0" fill="none" stroke="#ffffff" stroke-width="3" opacity=".7"/>'
    # marcas de nivel
    + ''.join(f'<line x1="160" y1="{170+_i*18}" x2="172" y2="{170+_i*18}" stroke="{{d}}" stroke-width="2" opacity=".5"/>' for _i in range(3))
    # canalón que llena el depósito + gota entrando
    + '<path d="M120 70 h70 v10 h-60 v20" fill="none" stroke="{d}" stroke-width="4" stroke-linecap="round"/>'
    '<path d="M130 104 q6 12 0 20 a10 10 0 1 1 0 -20z" fill="{glass}"/>'
    # grifo con chorro y charco
    + '<rect x="300" y="196" width="26" height="9" rx="3" fill="{d}"/>'
    '<rect x="322" y="196" width="9" height="20" rx="3" fill="{d}"/>'
    '<path d="M326 216 q-6 10 0 18 q6 -8 0 -18z" fill="{glass}"/>'
    '<ellipse cx="326" cy="238" rx="16" ry="4" fill="{glass}"/>'
)

# ---- B. Pasiva envolvente ----
def building(x, y, w, h, roof="{p}"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#ffffff" stroke="{{d}}" stroke-width="3"/>'
    )

M["B.1.1"] = sun(410, 58) + ground() + (
    # ventana con lamas/toldo exterior
    '<rect x="150" y="80" width="180" height="150" rx="8" fill="#ffffff" stroke="{d}" stroke-width="4"/>'
    '<rect x="165" y="120" width="150" height="105" fill="{glass}"/>'
    '<line x1="240" y1="120" x2="240" y2="225" stroke="#ffffff" stroke-width="4"/>'
    '<line x1="165" y1="172" x2="315" y2="172" stroke="#ffffff" stroke-width="4"/>'
    # lamas exteriores
    + ''.join(f'<rect x="150" y="{92+i*14}" width="180" height="7" rx="3" fill="{{p}}" opacity=".9"/>' for i in range(4))
)

M["B.1.2"] = sun(60, 58) + ground() + (
    '<rect x="150" y="80" width="180" height="150" rx="8" fill="#ffffff" stroke="{d}" stroke-width="4"/>'
    '<rect x="165" y="95" width="150" height="130" fill="{glass}"/>'
    # estor interior bajado a medias
    + '<rect x="165" y="95" width="150" height="60" fill="{p}" opacity=".85"/>'
    + ''.join(f'<line x1="165" y1="{110+i*14}" x2="315" y2="{110+i*14}" stroke="{{d}}" stroke-width="2" opacity=".5"/>' for i in range(3))
    + '<rect x="232" y="95" width="16" height="12" fill="{d}"/>'
)

M["B.1.3"] = ground() + sun(410, 56) + (
    # carpintería doble vidrio
    '<rect x="150" y="70" width="180" height="160" rx="8" fill="{p}"/>'
    '<rect x="163" y="83" width="154" height="134" rx="4" fill="{glass}"/>'
    '<rect x="171" y="91" width="138" height="118" rx="3" fill="#ffffff" opacity=".55"/>'
    '<line x1="240" y1="83" x2="240" y2="217" stroke="{p}" stroke-width="8"/>'
    '<line x1="163" y1="150" x2="317" y2="150" stroke="{p}" stroke-width="8"/>'
    '<circle cx="228" cy="150" r="6" fill="{d}"/>'
)

def roofline(x, y, w):
    return f'<rect x="{x}" y="{y}" width="{w}" height="120" rx="6" fill="#ffffff" stroke="{{d}}" stroke-width="3"/>'

M["B.2.1"] = sun(240, 66) + (
    # edificio con cubierta clara reflejando
    '<rect x="120" y="150" width="240" height="120" rx="6" fill="#ffffff" stroke="{d}" stroke-width="3"/>'
    '<rect x="110" y="132" width="260" height="22" rx="6" fill="#f4f7fb" stroke="{d}" stroke-width="3"/>'
    '<line x1="240" y1="96" x2="180" y2="132" stroke="{sun}" stroke-width="5" stroke-linecap="round"/>'
    '<line x1="240" y1="96" x2="300" y2="132" stroke="{sun}" stroke-width="5" stroke-linecap="round"/>'
    + ''.join(f'<rect x="{150+i*60}" y="185" width="34" height="34" rx="4" fill="{{glass}}"/>' for i in range(3))
)

M["B.2.2"] = sun(410, 58) + (
    # edificio con cubierta vegetal
    '<rect x="120" y="150" width="240" height="120" rx="6" fill="#ffffff" stroke="{d}" stroke-width="3"/>'
    '<rect x="110" y="120" width="260" height="34" rx="8" fill="{ground}" stroke="{d}" stroke-width="3"/>'
    + ''.join(f'<circle cx="{130+i*30}" cy="128" r="10" fill="{{p}}"/>' for i in range(9))
    + ''.join(f'<circle cx="{145+i*30}" cy="132" r="8" fill="{{d}}"/>' for i in range(8))
    + ''.join(f'<rect x="{150+i*60}" y="185" width="34" height="34" rx="4" fill="{{glass}}"/>' for i in range(3))
)

M["B.3"] = ground() + sun(58, 60) + (
    # sección de muro: exterior soleado | aislamiento | interior en confort
    # sol calienta por fuera, el calor se frena en el aislamiento
    ''.join(f'<path d="M40 {96+_i*34} h96" stroke="{{sun}}" stroke-width="4" stroke-linecap="round" opacity=".85"/><path d="M128 {90+_i*34} l10 6 l-10 6" fill="none" stroke="{{sun}}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>' for _i in range(3))
    # hoja exterior
    + '<rect x="150" y="72" width="30" height="156" fill="#d8cbb8"/>'
    # aislamiento (capa gruesa acolchada)
    '<rect x="180" y="72" width="72" height="156" fill="{p}"/>'
    + ''.join(f'<path d="M180 {80+_i*20} q36 12 72 0" stroke="#ffffff" stroke-width="3" fill="none" opacity=".55"/>' for _i in range(8))
    # hoja interior
    + '<rect x="252" y="72" width="26" height="156" fill="#e9e2d5"/>'
    '<rect x="150" y="72" width="128" height="156" fill="none" stroke="{d}" stroke-width="3"/>'
    # interior confortable: termómetro ok
    + '<rect x="360" y="120" width="16" height="70" rx="8" fill="#ffffff" stroke="{d}" stroke-width="3"/>'
    '<circle cx="368" cy="196" r="15" fill="{p}"/>'
    '<rect x="364" y="140" width="8" height="52" rx="4" fill="{p}"/>'
    '<path d="M300 150 q30 -8 52 0" stroke="{p}" stroke-width="3" fill="none" stroke-dasharray="2 6"/>'
)

# ---- C. Pasiva interior ----
M["C.1.1"] = sun(60, 58) + ground() + (
    # ventana abierta con flechas de aire + reloj
    '<rect x="150" y="80" width="180" height="150" rx="8" fill="#ffffff" stroke="{d}" stroke-width="4"/>'
    '<rect x="163" y="93" width="70" height="124" fill="{glass}"/>'
    '<rect x="247" y="93" width="70" height="124" fill="{glass}" opacity=".6"/>'
    '<path d="M247 155 l70 -18 l0 96 l-70 -18z" fill="{p}" opacity=".85"/>'
    '<path d="M60 150 q40 -14 80 0" stroke="{p}" stroke-width="5" fill="none" marker-end=""/>'
    '<path d="M132 143 l14 7 l-14 7" fill="none" stroke="{p}" stroke-width="5" stroke-linecap="round"/>'
    '<path d="M60 185 q40 -14 80 0" stroke="{d}" stroke-width="5" fill="none"/>'
    '<path d="M132 178 l14 7 l-14 7" fill="none" stroke="{d}" stroke-width="5" stroke-linecap="round"/>'
    '<circle cx="400" cy="150" r="30" fill="#ffffff" stroke="{d}" stroke-width="4"/>'
    '<line x1="400" y1="150" x2="400" y2="132" stroke="{d}" stroke-width="4" stroke-linecap="round"/>'
    '<line x1="400" y1="150" x2="414" y2="158" stroke="{d}" stroke-width="4" stroke-linecap="round"/>'
)

M["C.1.2"] = (
    # cielo nocturno oscuro
    '<rect width="480" height="300" fill="#1e2c40"/>'
    '<rect x="0" y="232" width="480" height="68" fill="#141d2b"/>'
    # estrellas
    + ''.join(f'<circle cx="{54+_i*52}" cy="{34+((_i*41)%54)}" r="{1.6+(_i%2)}" fill="#f2f5ff" opacity=".85"/>' for _i in range(8))
    # luna creciente (círculo claro tallado por otro del color del cielo)
    + '<circle cx="402" cy="64" r="30" fill="#eef0dc"/>'
    '<circle cx="390" cy="56" r="27" fill="#1e2c40"/>'
    # ventana abierta con flujo de aire (purga nocturna)
    + '<rect x="150" y="96" width="180" height="140" rx="8" fill="#f4f7fb" stroke="#0d1420" stroke-width="4"/>'
    '<rect x="163" y="109" width="70" height="114" fill="{glass}"/>'
    '<rect x="247" y="109" width="70" height="114" fill="{glass}" opacity=".5"/>'
    '<path d="M247 166 l70 -16 l0 74 l-70 -16z" fill="#cfe0ee"/>'
    # flechas de aire saliendo (claras para verse sobre el cielo)
    '<path d="M108 150 q40 -14 62 0" stroke="#cfe0ee" stroke-width="5" fill="none"/>'
    '<path d="M162 143 l14 7 l-14 7" fill="none" stroke="#cfe0ee" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M108 190 q40 14 62 0" stroke="#cfe0ee" stroke-width="5" fill="none"/>'
    '<path d="M162 183 l14 7 l-14 7" fill="none" stroke="#cfe0ee" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
)

M["C.1.3"] = ground() + sun(410, 56) + (
    # planta con aulas y flechas de reubicación
    '<rect x="90" y="90" width="140" height="140" rx="6" fill="#ffffff" stroke="{d}" stroke-width="3"/>'
    '<rect x="250" y="90" width="140" height="140" rx="6" fill="{p}" opacity=".18" stroke="{d}" stroke-width="3"/>'
    '<line x1="160" y1="90" x2="160" y2="230" stroke="{d}" stroke-width="2" opacity=".4"/>'
    '<line x1="320" y1="90" x2="320" y2="230" stroke="{d}" stroke-width="2" opacity=".4"/>'
    '<circle cx="125" cy="160" r="12" fill="{sun}"/><text x="118" y="220" font-family="sans-serif" font-size="20" fill="{d}">☀</text>'
    '<path d="M232 130 q20 -10 40 0" stroke="{p}" stroke-width="6" fill="none"/>'
    '<path d="M264 122 l12 8 l-12 8" fill="none" stroke="{p}" stroke-width="6" stroke-linecap="round"/>'
    '<circle cx="355" cy="160" r="12" fill="{p}"/>'
)

M["C.1.4"] = ground() + sun(60, 58) + (
    # persiana bajada + enchufe/carga
    '<rect x="120" y="80" width="150" height="150" rx="8" fill="#ffffff" stroke="{d}" stroke-width="4"/>'
    + ''.join(f'<rect x="133" y="{95+i*15}" width="124" height="9" rx="3" fill="{{p}}" opacity=".8"/>' for i in range(7))
    + '<rect x="320" y="120" width="90" height="90" rx="10" fill="{p}"/>'
    '<circle cx="352" cy="155" r="7" fill="#ffffff"/><circle cx="378" cy="155" r="7" fill="#ffffff"/>'
    '<rect x="358" y="175" width="14" height="18" rx="3" fill="#ffffff"/>'
)

M["C.2"] = ground() + (
    # medidor / sensor con lecturas
    '<rect x="150" y="80" width="180" height="150" rx="14" fill="#ffffff" stroke="{d}" stroke-width="4"/>'
    '<path d="M180 165 a60 60 0 0 1 120 0" fill="none" stroke="{ground}" stroke-width="12"/>'
    '<path d="M180 165 a60 60 0 0 1 78 -55" fill="none" stroke="{p}" stroke-width="12" stroke-linecap="round"/>'
    '<line x1="240" y1="165" x2="272" y2="128" stroke="{d}" stroke-width="5" stroke-linecap="round"/>'
    '<circle cx="240" cy="165" r="8" fill="{d}"/>'
    '<text x="240" y="212" font-family="sans-serif" font-size="20" font-weight="700" fill="{d}" text-anchor="middle">CO₂ · Tª · HR</text>'
    + sun(410, 56)
)

# ---- D. Activa ----
M["D.1.1"] = ground() + (
    # ventilador de techo
    '<line x1="240" y1="70" x2="240" y2="110" stroke="{d}" stroke-width="6"/>'
    '<circle cx="240" cy="120" r="16" fill="{d}"/>'
    '<ellipse cx="175" cy="120" rx="70" ry="18" fill="{p}"/>'
    '<ellipse cx="305" cy="120" rx="70" ry="18" fill="{p}" opacity=".8"/>'
    '<circle cx="240" cy="120" r="9" fill="{sun}"/>'
    '<path d="M150 175 q90 40 180 0" stroke="{p}" stroke-width="4" fill="none" stroke-dasharray="2 8" stroke-linecap="round"/>'
    '<path d="M170 205 q70 34 140 0" stroke="{p}" stroke-width="4" fill="none" stroke-dasharray="2 8" stroke-linecap="round"/>'
)

M["D.1.2"] = ground() + sun(410, 56) + (
    # extractor / conducto
    '<rect x="130" y="110" width="120" height="120" rx="10" fill="#ffffff" stroke="{d}" stroke-width="3"/>'
    '<circle cx="190" cy="170" r="42" fill="{p}" opacity=".18" stroke="{d}" stroke-width="3"/>'
    + ''.join(f'<path d="M190 170 L{190+38} {170} A38 38 0 0 0 {190+27} {170-27} Z" fill="{{p}}" opacity=".8" transform="rotate({a} 190 170)"/>' for a in (0,72,144,216,288))
    + '<circle cx="190" cy="170" r="10" fill="{d}"/>'
    '<rect x="250" y="150" width="130" height="40" rx="8" fill="{ground}" stroke="{d}" stroke-width="3"/>'
    '<path d="M270 170 h90" stroke="{p}" stroke-width="4" stroke-dasharray="2 8" stroke-linecap="round"/>'
    '<path d="M352 162 l12 8 l-12 8" fill="none" stroke="{p}" stroke-width="4" stroke-linecap="round"/>'
)

M["D.1.3"] = ground() + sun(410, 56) + (
    # unidad de ventilación mecánica (caja + conductos)
    '<rect x="120" y="110" width="150" height="120" rx="10" fill="#ffffff" stroke="{d}" stroke-width="3"/>'
    '<rect x="138" y="128" width="55" height="84" rx="4" fill="{glass}"/>'
    + ''.join(f'<line x1="146" y1="{138+i*14}" x2="185" y2="{138+i*14}" stroke="{{d}}" stroke-width="3" opacity=".5"/>' for i in range(5))
    + '<circle cx="230" cy="170" r="22" fill="{p}" opacity=".25" stroke="{d}" stroke-width="3"/>'
    '<circle cx="230" cy="170" r="6" fill="{d}"/>'
    '<rect x="270" y="140" width="120" height="24" rx="6" fill="{ground}" stroke="{d}" stroke-width="2"/>'
    '<rect x="270" y="180" width="120" height="24" rx="6" fill="{ground}" stroke="{d}" stroke-width="2"/>'
    '<path d="M285 152 h80" stroke="{p}" stroke-width="4" stroke-dasharray="2 7" stroke-linecap="round"/>'
    '<path d="M365 192 h-80" stroke="{d}" stroke-width="4" stroke-dasharray="2 7" stroke-linecap="round"/>'
)

M["D.1.4"] = ground() + sun(60, 58) + (
    # ventana + ventilador (híbrido)
    '<rect x="130" y="90" width="150" height="140" rx="8" fill="#ffffff" stroke="{d}" stroke-width="4"/>'
    '<rect x="143" y="103" width="124" height="114" fill="{glass}" opacity=".7"/>'
    '<path d="M143 155 l124 -16 l0 78 l-124 -16z" fill="{p}" opacity=".8"/>'
    '<circle cx="360" cy="150" r="40" fill="{p}" opacity=".18" stroke="{d}" stroke-width="3"/>'
    + ''.join(f'<path d="M360 150 L{360+36} 150 A36 36 0 0 0 {360+25} {150-25} Z" fill="{{p}}" opacity=".85" transform="rotate({a} 360 150)"/>' for a in (0,90,180,270))
    + '<circle cx="360" cy="150" r="9" fill="{d}"/>'
)

M["D.2"] = ground() + sun(410, 56) + (
    # split de climatización + aire frío
    '<rect x="120" y="110" width="240" height="66" rx="14" fill="#ffffff" stroke="{d}" stroke-width="3"/>'
    '<rect x="120" y="150" width="240" height="10" fill="{p}"/>'
    '<circle cx="330" cy="128" r="4" fill="{p}"/>'
    + ''.join(f'<path d="M{160+i*40} 182 q-8 20 0 40" stroke="{{glass}}" stroke-width="6" fill="none" stroke-linecap="round"/>' for i in range(5))
    + '<text x="240" y="140" font-family="sans-serif" font-size="18" fill="{d}" text-anchor="middle" opacity=".6">✳</text>'
)

M["D.3"] = sun(410, 58) + ground() + (
    # placas fotovoltaicas en cubierta
    '<rect x="120" y="150" width="240" height="90" rx="6" fill="#ffffff" stroke="{d}" stroke-width="3"/>'
    '<g transform="skewX(-12)">'
    + ''.join(
        f'<rect x="{175+ (i%3)*66}" y="{80+ (i//3)*40}" width="60" height="34" rx="3" fill="{{p}}" stroke="{{d}}" stroke-width="2"/>'
        for i in range(6))
    + '</g>'
    + ''.join(f'<line x1="240" y1="60" x2="{200+i*30}" y2="110" stroke="{{sun}}" stroke-width="3" opacity=".5" stroke-linecap="round"/>' for i in range(3))
)

M["D.4"] = ground() + sun(410, 56) + (
    # panel de control / automatización
    '<rect x="140" y="80" width="200" height="150" rx="14" fill="#ffffff" stroke="{d}" stroke-width="4"/>'
    '<rect x="160" y="100" width="160" height="50" rx="6" fill="{glass}"/>'
    '<path d="M172 128 l14 -16 l12 12 l16 -22 l14 26" stroke="{p}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    + ''.join(f'<circle cx="{175+i*40}" cy="180" r="13" fill="{{p}}" opacity="{0.9 - i*0.2}"/>' for i in range(4))
    + '<rect x="160" y="205" width="160" height="10" rx="5" fill="{ground}"/>'
    '<rect x="160" y="205" width="96" height="10" rx="5" fill="{p}"/>'
)


def main():
    n = 0
    for code, inner in M.items():
        g = code[0]
        svg = frame(g, inner)
        fname = code.replace(".", "-") + ".svg"
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as fh:
            fh.write(svg)
        n += 1
    print(f"OK — {n} ilustraciones SVG -> assets/img/")


if __name__ == "__main__":
    main()
