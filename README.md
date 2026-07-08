# TooCool4School — Catálogo de estrategias contra el sobrecalentamiento en colegios

App web interactiva con un catálogo de estrategias para **mitigar el sobrecalentamiento en centros educativos**, organizado de lo pasivo a lo activo. Cada estrategia tiene su **ficha editable** en el repositorio.

Los datos de partida provienen del documento *«Catálogo directo de estrategias tipo para mitigar el sobrecalentamiento en centros educativos de Bizkaia»*.

## Cómo verla

Abre `index.html` en el navegador (doble clic). No necesita servidor ni conexión: la app carga el bundle `data/estrategias.js`.

También puede publicarse tal cual en **GitHub Pages** (Settings → Pages → rama y carpeta raíz).

## Funciones de la app

- **Buscador** por texto (título, descripción, materiales, criterios, referencias…).
- **Filtros** por grupo (A/B/C/D), impacto y coste.
- **Navegación lateral** por categorías y subcategorías.
- **Ficha detallada** (modal) con todos los apartados. El enlace incluye el código (`index.html#B.2.1`) para compartir una estrategia concreta.

## Estructura del catálogo

| Grupo | Categoría |
|-------|-----------|
| **A** | Pasiva exterior (sombra, vegetación, pavimentos, refugios climáticos, agua) |
| **B** | Pasiva envolvente (huecos, cubierta, cerramientos) |
| **C** | Pasiva interior (uso y operación, monitorización) |
| **D** | Activa (ventilación, climatización, energía, control) |

## Cómo editar o añadir estrategias

**Una ficha = un archivo JSON** en `data/estrategias/`. El nombre del archivo es el código con guiones (p. ej. `B-2-1.json` para la estrategia `B.2.1`).

### Editar una ficha existente

1. Abre el `.json` de la estrategia en `data/estrategias/`.
2. Modifica los campos que quieras (ver esquema abajo).
3. Regenera el bundle:
   ```bash
   python3 build.py
   ```
4. Recarga `index.html`.

### Añadir una estrategia nueva

1. Copia una ficha existente en `data/estrategias/` con el nuevo código (p. ej. `A-6.json`).
2. Rellena los campos.
3. Ejecuta `python3 build.py`. La app la ordena y la coloca en su grupo automáticamente.

### Esquema de una ficha

```json
{
  "codigo": "B.2.1",              // código jerárquico (obligatorio, único)
  "grupo": "B",                  // A | B | C | D
  "subgrupo": "B.2",             // código de la subcategoría
  "subgrupo_nombre": "Cubierta", // nombre de la subcategoría
  "titulo": "Cubierta fría / reflectante",
  "impacto": "Medio-alto",       // se usa en filtros (contiene Alto/Medio/Bajo)
  "coste": "Medio",              // se usa en filtros (contiene Alto/Medio/Bajo)
  "plazo": "Corto-medio plazo",
  "descripcion": "Texto introductorio…",
  "beneficios":   ["…", "…"],    // lista
  "limitaciones": ["…", "…"],    // lista
  "criterios":    ["…", "…"],    // criterios de aplicación y recomendaciones de diseño
  "coste_detalle": "Texto sobre coste y rapidez…",
  "referencias":  ["…", "…"],    // referencias o casos de estudio
  "ejemplos_mercado": ["…", "…"] // materiales, sistemas o productos del mercado
}
```

> El campo `grupo_nombre` se rellena solo al construir; no hace falta escribirlo.

## Archivos del proyecto

```
index.html              La app (HTML + CSS + JS, sin dependencias)
build.py                Genera data/estrategias.js a partir de las fichas
data/estrategias/*.json Una ficha editable por estrategia (fuente de la verdad)
data/estrategias.js     Bundle generado que carga la app (no editar a mano)
```

## Nota sobre el contenido

Las fichas recogen la información del documento de partida (descripción, impacto, coste/rapidez, cuándo aplicar y condicionantes) y la amplían con criterios de diseño, referencias y ejemplos orientativos de mercado. **Los ejemplos de productos y marcas son orientativos**: conviene contrastarlos y adaptarlos a cada centro y a las condiciones de contratación.
