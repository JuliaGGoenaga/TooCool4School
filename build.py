#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — Genera el bundle de datos de la app a partir de las fichas.

Lee todas las fichas JSON de data/estrategias/*.json y las agrupa en un
único fichero data/estrategias.js (window.ESTRATEGIAS = [...]).

Ese bundle es lo que carga index.html, de modo que la app funciona
abriendo el HTML directamente (file://) sin necesidad de servidor.

Uso:
    python3 build.py

Ejecuta este script cada vez que crees o edites una ficha para regenerar
el bundle. No necesitas ninguna dependencia externa.
"""
import json
import os
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
FICHAS_DIR = os.path.join(ROOT, "data", "estrategias")
OUT_JS = os.path.join(ROOT, "data", "estrategias.js")

# Orden de los grupos y clave de ordenación de códigos (A.3.1 antes que A.4, etc.)
GRUPO_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3}


def code_key(codigo):
    """Ordena por grupo y luego por número: A.1, A.3.1, A.3.2, A.4..."""
    grupo = codigo[0]
    partes = codigo[1:].lstrip(".").split(".")
    nums = [int(p) for p in partes if p.isdigit()]
    return (GRUPO_ORDER.get(grupo, 99), nums)


def main():
    archivos = sorted(glob.glob(os.path.join(FICHAS_DIR, "*.json")))
    fichas = []
    for ruta in archivos:
        with open(ruta, "r", encoding="utf-8") as fh:
            try:
                fichas.append(json.load(fh))
            except json.JSONDecodeError as e:
                raise SystemExit(f"Error de JSON en {os.path.basename(ruta)}: {e}")

    fichas.sort(key=lambda f: code_key(f["codigo"]))

    datos_json = json.dumps(fichas, ensure_ascii=False, indent=2)
    contenido = (
        "// ARCHIVO GENERADO AUTOMÁTICAMENTE por build.py — NO EDITAR A MANO.\n"
        "// Edita las fichas en data/estrategias/*.json y ejecuta: python3 build.py\n"
        "window.ESTRATEGIAS = " + datos_json + ";\n"
    )
    with open(OUT_JS, "w", encoding="utf-8") as fh:
        fh.write(contenido)

    print(f"OK — {len(fichas)} fichas -> {os.path.relpath(OUT_JS, ROOT)}")


if __name__ == "__main__":
    main()
