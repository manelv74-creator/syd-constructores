
import re, json

# ── 32-week data for all 5 zones ─────────────────────────────────────────
ZONES = [
  {
    "zone": "Zona 1: Cochera", "emoji": "🏠",
    "tasks": ["A01 Preliminares", "A02 Demoliciones", "A03 Zapatas aisladas", "A03 Zapatas aisladas", "A04 Zapatas corridas", "A04 Zapatas corridas", "A05 Albañilerías", "A05 Albañilerías", "A06 Estructura de Acero", "A06 Estructura de Acero", "A06 Estructura de Acero", "A06 Estructura de Acero", "A07 Losa aligerada", "A07 Losa aligerada", "A08 Durock en cubierta", "A08 Durock en cubierta", "A09 Instalación Eléctrica", "A09 Instalación Eléctrica", "A09 Accesorios Eléctricos", "A09 Tableros/Interrupt.", "A10 Inst. Hidráulicas", "A10 Inst. Hidráulicas", "A10 Inst. Sanitarias", "A10 Inst. Sanitarias", "A10 Inst. Pluviales", "A10 Inst. Pluviales", "A11 Recubrimi./Pintura", "A11 Recubrimi./Pintura", "A12 Herrería", "A12 Herrería", "A12 Herrería", "A13 Limpieza"],
    "details": [
      ["A01 Preliminares", "Ejecución correspondiente a la partida A01 Preliminares de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A02 Demoliciones", "Ejecución correspondiente a la partida A02 Demoliciones de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A03 Zapatas aisladas", "Ejecución correspondiente a la partida A03 Zapatas aisladas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A03 Zapatas aisladas", "Ejecución correspondiente a la partida A03 Zapatas aisladas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A04 Zapatas corridas", "Ejecución correspondiente a la partida A04 Zapatas corridas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A04 Zapatas corridas", "Ejecución correspondiente a la partida A04 Zapatas corridas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A05 Albañilerías", "Ejecución correspondiente a la partida A05 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A05 Albañilerías", "Ejecución correspondiente a la partida A05 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A06 Estructura de Acero", "Ejecución correspondiente a la partida A06 Estructura de Acero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A06 Estructura de Acero", "Ejecución correspondiente a la partida A06 Estructura de Acero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A06 Estructura de Acero", "Ejecución correspondiente a la partida A06 Estructura de Acero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A06 Estructura de Acero", "Ejecución correspondiente a la partida A06 Estructura de Acero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A07 Losa aligerada", "Ejecución correspondiente a la partida A07 Losa aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A07 Losa aligerada", "Ejecución correspondiente a la partida A07 Losa aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A08 Durock en cubierta", "Ejecución correspondiente a la partida A08 Durock en cubierta de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A08 Durock en cubierta", "Ejecución correspondiente a la partida A08 Durock en cubierta de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A09 Instalación Eléctrica", "Ejecución correspondiente a la partida A09 Instalación Eléctrica de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A09 Instalación Eléctrica", "Ejecución correspondiente a la partida A09 Instalación Eléctrica de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A09 Accesorios Eléctricos", "Ejecución correspondiente a la partida A09 Accesorios Eléctricos de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A09 Tableros/Interrupt.", "Ejecución correspondiente a la partida A09 Tableros/Interrupt. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A10 Inst. Hidráulicas", "Ejecución correspondiente a la partida A10 Inst. Hidráulicas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A10 Inst. Hidráulicas", "Ejecución correspondiente a la partida A10 Inst. Hidráulicas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A10 Inst. Sanitarias", "Ejecución correspondiente a la partida A10 Inst. Sanitarias de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A10 Inst. Sanitarias", "Ejecución correspondiente a la partida A10 Inst. Sanitarias de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A10 Inst. Pluviales", "Ejecución correspondiente a la partida A10 Inst. Pluviales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A10 Inst. Pluviales", "Ejecución correspondiente a la partida A10 Inst. Pluviales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A11 Recubrimi./Pintura", "Ejecución correspondiente a la partida A11 Recubrimi./Pintura de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A11 Recubrimi./Pintura", "Ejecución correspondiente a la partida A11 Recubrimi./Pintura de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A12 Herrería", "Ejecución correspondiente a la partida A12 Herrería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A12 Herrería", "Ejecución correspondiente a la partida A12 Herrería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A12 Herrería", "Ejecución correspondiente a la partida A12 Herrería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["A13 Limpieza", "Ejecución correspondiente a la partida A13 Limpieza de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
    ]
  },
  {
    "zone": "Zona 2: Baño Ppal", "emoji": "🚿",
    "tasks": ["F01 Preliminares", "F02 Desmontajes", "F03 Demoliciones", "F04 Zapata corrida", "F04 Zapata corrida", "F05 Albañilerías", "F05 Albañilerías", "F05 Albañilerías", "F06 Losa aligerada", "F06 Losa aligerada", "H01 Desmontaje", "H02 Estructura Acero", "H02 Estructura Acero", "H03 Durock Cubierta", "F07 Inst. Eléctricas", "F07 Inst. Eléctricas", "F07 Accesorios Eléctr.", "F07 Tablero/Interrupt.", "F08 Inst. Hidráulicas", "F08 Inst. Sanitarias", "F08 Inst. Pluviales", "F08 Inst. Pluviales", "F08 Accesorios Sanit.", "F08 Accesorios Sanit.", "F09 Recubrim./Pintura", "F09 Recubrim./Pintura", "F10 Cancelería", "F10 Cancelería", "F11 Carpintería", "F11 Carpintería", "F12 Lambrín WPC", "F13 Limpieza"],
    "details": [
      ["F01 Preliminares", "Ejecución correspondiente a la partida F01 Preliminares de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F02 Desmontajes", "Ejecución correspondiente a la partida F02 Desmontajes de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F03 Demoliciones", "Ejecución correspondiente a la partida F03 Demoliciones de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F04 Zapata corrida", "Ejecución correspondiente a la partida F04 Zapata corrida de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F04 Zapata corrida", "Ejecución correspondiente a la partida F04 Zapata corrida de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F05 Albañilerías", "Ejecución correspondiente a la partida F05 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F05 Albañilerías", "Ejecución correspondiente a la partida F05 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F05 Albañilerías", "Ejecución correspondiente a la partida F05 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F06 Losa aligerada", "Ejecución correspondiente a la partida F06 Losa aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F06 Losa aligerada", "Ejecución correspondiente a la partida F06 Losa aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["H01 Desmontaje", "Ejecución correspondiente a la partida H01 Desmontaje de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["H02 Estructura Acero", "Ejecución correspondiente a la partida H02 Estructura Acero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["H02 Estructura Acero", "Ejecución correspondiente a la partida H02 Estructura Acero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["H03 Durock Cubierta", "Ejecución correspondiente a la partida H03 Durock Cubierta de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F07 Inst. Eléctricas", "Ejecución correspondiente a la partida F07 Inst. Eléctricas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F07 Inst. Eléctricas", "Ejecución correspondiente a la partida F07 Inst. Eléctricas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F07 Accesorios Eléctr.", "Ejecución correspondiente a la partida F07 Accesorios Eléctr. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F07 Tablero/Interrupt.", "Ejecución correspondiente a la partida F07 Tablero/Interrupt. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F08 Inst. Hidráulicas", "Ejecución correspondiente a la partida F08 Inst. Hidráulicas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F08 Inst. Sanitarias", "Ejecución correspondiente a la partida F08 Inst. Sanitarias de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F08 Inst. Pluviales", "Ejecución correspondiente a la partida F08 Inst. Pluviales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F08 Inst. Pluviales", "Ejecución correspondiente a la partida F08 Inst. Pluviales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F08 Accesorios Sanit.", "Ejecución correspondiente a la partida F08 Accesorios Sanit. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F08 Accesorios Sanit.", "Ejecución correspondiente a la partida F08 Accesorios Sanit. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F09 Recubrim./Pintura", "Ejecución correspondiente a la partida F09 Recubrim./Pintura de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F09 Recubrim./Pintura", "Ejecución correspondiente a la partida F09 Recubrim./Pintura de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F10 Cancelería", "Ejecución correspondiente a la partida F10 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F10 Cancelería", "Ejecución correspondiente a la partida F10 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F11 Carpintería", "Ejecución correspondiente a la partida F11 Carpintería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F11 Carpintería", "Ejecución correspondiente a la partida F11 Carpintería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F12 Lambrín WPC", "Ejecución correspondiente a la partida F12 Lambrín WPC de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["F13 Limpieza", "Ejecución correspondiente a la partida F13 Limpieza de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
    ]
  },
  {
    "zone": "Zona 3: Recámara 2", "emoji": "🛏",
    "tasks": ["B01/C01 Preliminar.", "B02 Desmontajes", "B03 Demoliciones", "B04 Zapata Corrida", "B05 Losa Rampa", "B06 Albañilerías", "C02 Albañilerías", "C02 Albañilerías", "C03 Losa Aligerada", "C03 Losa Aligerada", "C04 Inst. Eléctricas", "B07 Inst. Eléctricas", "C04 Inst. Eléctricas", "C04 Accesori. Eléct.", "B07 Accesori. Eléct.", "C04 Tablero", "C05 Inst. Pluviales", "C05 Inst. Pluviales", "C06 Voz y Datos", "B08 Recubrim./Pint.", "C07 Recubrim./Pint.", "C07 Recubrim./Pint.", "B09 Cancelería", "B09 Cancelería", "C08 Cancelería", "C08 Cancelería", "B10 Lambrín WPC", "B10 Lambrín WPC", "Detalle Lambrín", "Ajustes finales", "B11 Limpieza", "C09 Limpieza"],
    "details": [
      ["B01/C01 Preliminar.", "Ejecución correspondiente a la partida B01/C01 Preliminar. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B02 Desmontajes", "Ejecución correspondiente a la partida B02 Desmontajes de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B03 Demoliciones", "Ejecución correspondiente a la partida B03 Demoliciones de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B04 Zapata Corrida", "Ejecución correspondiente a la partida B04 Zapata Corrida de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B05 Losa Rampa", "Ejecución correspondiente a la partida B05 Losa Rampa de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B06 Albañilerías", "Ejecución correspondiente a la partida B06 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C02 Albañilerías", "Ejecución correspondiente a la partida C02 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C02 Albañilerías", "Ejecución correspondiente a la partida C02 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C03 Losa Aligerada", "Ejecución correspondiente a la partida C03 Losa Aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C03 Losa Aligerada", "Ejecución correspondiente a la partida C03 Losa Aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C04 Inst. Eléctricas", "Ejecución correspondiente a la partida C04 Inst. Eléctricas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B07 Inst. Eléctricas", "Ejecución correspondiente a la partida B07 Inst. Eléctricas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C04 Inst. Eléctricas", "Ejecución correspondiente a la partida C04 Inst. Eléctricas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C04 Accesori. Eléct.", "Ejecución correspondiente a la partida C04 Accesori. Eléct. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B07 Accesori. Eléct.", "Ejecución correspondiente a la partida B07 Accesori. Eléct. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C04 Tablero", "Ejecución correspondiente a la partida C04 Tablero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C05 Inst. Pluviales", "Ejecución correspondiente a la partida C05 Inst. Pluviales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C05 Inst. Pluviales", "Ejecución correspondiente a la partida C05 Inst. Pluviales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C06 Voz y Datos", "Ejecución correspondiente a la partida C06 Voz y Datos de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B08 Recubrim./Pint.", "Ejecución correspondiente a la partida B08 Recubrim./Pint. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C07 Recubrim./Pint.", "Ejecución correspondiente a la partida C07 Recubrim./Pint. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C07 Recubrim./Pint.", "Ejecución correspondiente a la partida C07 Recubrim./Pint. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B09 Cancelería", "Ejecución correspondiente a la partida B09 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B09 Cancelería", "Ejecución correspondiente a la partida B09 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C08 Cancelería", "Ejecución correspondiente a la partida C08 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C08 Cancelería", "Ejecución correspondiente a la partida C08 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B10 Lambrín WPC", "Ejecución correspondiente a la partida B10 Lambrín WPC de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B10 Lambrín WPC", "Ejecución correspondiente a la partida B10 Lambrín WPC de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["Detalle Lambrín", "Ejecución correspondiente a la partida Detalle Lambrín de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["Ajustes finales", "Ejecución correspondiente a la partida Ajustes finales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["B11 Limpieza", "Ejecución correspondiente a la partida B11 Limpieza de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["C09 Limpieza", "Ejecución correspondiente a la partida C09 Limpieza de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
    ]
  },
  {
    "zone": "Zona 4: Recámara 1", "emoji": "🛏",
    "tasks": ["G01 Preliminares", "G02 Desmontajes", "G03 Demoliciones", "G04 Zapata corrida", "G04 Zapata corrida", "G05 Albañilerías", "G05 Albañilerías", "G06 Losa aligerada", "G06 Losa aligerada", "H01 Desmontaje", "H02 Estructura Acero", "H03 Durock Cubierta", "G07 Inst. Eléctricas", "G07 Inst. Eléctricas", "G07 Accesorios Eléc.", "G07 Tablero", "G08 Inst. Hidráulicas", "G08 Inst. Sanitarias", "G08 Inst. Pluviales", "G08 Inst. Pluviales", "G08 Accesorios San.", "G09 Recubrim./Pint.", "G09 Recubrim./Pint.", "G09 Recubrim./Pint.", "G10 Cancelería", "G10 Cancelería", "G11 Carpintería", "G11 Carpintería", "Adecuaciones", "Pruebas generales", "Retiro material", "G12 Limpieza"],
    "details": [
      ["G01 Preliminares", "Ejecución correspondiente a la partida G01 Preliminares de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G02 Desmontajes", "Ejecución correspondiente a la partida G02 Desmontajes de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G03 Demoliciones", "Ejecución correspondiente a la partida G03 Demoliciones de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G04 Zapata corrida", "Ejecución correspondiente a la partida G04 Zapata corrida de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G04 Zapata corrida", "Ejecución correspondiente a la partida G04 Zapata corrida de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G05 Albañilerías", "Ejecución correspondiente a la partida G05 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G05 Albañilerías", "Ejecución correspondiente a la partida G05 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G06 Losa aligerada", "Ejecución correspondiente a la partida G06 Losa aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G06 Losa aligerada", "Ejecución correspondiente a la partida G06 Losa aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["H01 Desmontaje", "Ejecución correspondiente a la partida H01 Desmontaje de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["H02 Estructura Acero", "Ejecución correspondiente a la partida H02 Estructura Acero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["H03 Durock Cubierta", "Ejecución correspondiente a la partida H03 Durock Cubierta de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G07 Inst. Eléctricas", "Ejecución correspondiente a la partida G07 Inst. Eléctricas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G07 Inst. Eléctricas", "Ejecución correspondiente a la partida G07 Inst. Eléctricas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G07 Accesorios Eléc.", "Ejecución correspondiente a la partida G07 Accesorios Eléc. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G07 Tablero", "Ejecución correspondiente a la partida G07 Tablero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G08 Inst. Hidráulicas", "Ejecución correspondiente a la partida G08 Inst. Hidráulicas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G08 Inst. Sanitarias", "Ejecución correspondiente a la partida G08 Inst. Sanitarias de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G08 Inst. Pluviales", "Ejecución correspondiente a la partida G08 Inst. Pluviales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G08 Inst. Pluviales", "Ejecución correspondiente a la partida G08 Inst. Pluviales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G08 Accesorios San.", "Ejecución correspondiente a la partida G08 Accesorios San. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G09 Recubrim./Pint.", "Ejecución correspondiente a la partida G09 Recubrim./Pint. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G09 Recubrim./Pint.", "Ejecución correspondiente a la partida G09 Recubrim./Pint. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G09 Recubrim./Pint.", "Ejecución correspondiente a la partida G09 Recubrim./Pint. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G10 Cancelería", "Ejecución correspondiente a la partida G10 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G10 Cancelería", "Ejecución correspondiente a la partida G10 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G11 Carpintería", "Ejecución correspondiente a la partida G11 Carpintería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G11 Carpintería", "Ejecución correspondiente a la partida G11 Carpintería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["Adecuaciones", "Ejecución correspondiente a la partida Adecuaciones de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["Pruebas generales", "Ejecución correspondiente a la partida Pruebas generales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["Retiro material", "Ejecución correspondiente a la partida Retiro material de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["G12 Limpieza", "Ejecución correspondiente a la partida G12 Limpieza de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
    ]
  },
  {
    "zone": "Zona 5: Sala TV", "emoji": "📺",
    "tasks": ["D01/E01 Prelimina.", "D02 Desmontajes", "D03 Demoliciones", "D04 Zapatas Aisladas", "D05 Zapatas Corridas", "D06 Albañilerías", "E02 Albañilerías", "E02 Albañilerías", "D07 Losa Aligerada", "E03 Losa Aligerada", "E03 Losa Aligerada", "D08 Inst. Eléctricas", "E04 Inst. Eléctricas", "E04 Accesori. Eléct.", "D08 Acce./Tablero", "E04 Tablero", "E05 Inst. Pluviales", "E05 Inst. Pluviales", "E06 Voz y Datos", "D09 Recubrim./Pint.", "E07 Recubrim./Pint.", "E07 Recubrim./Pint.", "D10 Cancelería", "E08 Cancelería", "E08 Cancelería", "D11 Lambrín WPC", "E09 Lambrín WPC", "E09 Lambrín WPC", "D12 Herrería", "D12 Herrería", "D13 Limpieza", "E10 Limpieza"],
    "details": [
      ["D01/E01 Prelimina.", "Ejecución correspondiente a la partida D01/E01 Prelimina. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D02 Desmontajes", "Ejecución correspondiente a la partida D02 Desmontajes de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D03 Demoliciones", "Ejecución correspondiente a la partida D03 Demoliciones de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D04 Zapatas Aisladas", "Ejecución correspondiente a la partida D04 Zapatas Aisladas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D05 Zapatas Corridas", "Ejecución correspondiente a la partida D05 Zapatas Corridas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D06 Albañilerías", "Ejecución correspondiente a la partida D06 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E02 Albañilerías", "Ejecución correspondiente a la partida E02 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E02 Albañilerías", "Ejecución correspondiente a la partida E02 Albañilerías de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D07 Losa Aligerada", "Ejecución correspondiente a la partida D07 Losa Aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E03 Losa Aligerada", "Ejecución correspondiente a la partida E03 Losa Aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E03 Losa Aligerada", "Ejecución correspondiente a la partida E03 Losa Aligerada de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D08 Inst. Eléctricas", "Ejecución correspondiente a la partida D08 Inst. Eléctricas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E04 Inst. Eléctricas", "Ejecución correspondiente a la partida E04 Inst. Eléctricas de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E04 Accesori. Eléct.", "Ejecución correspondiente a la partida E04 Accesori. Eléct. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D08 Acce./Tablero", "Ejecución correspondiente a la partida D08 Acce./Tablero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E04 Tablero", "Ejecución correspondiente a la partida E04 Tablero de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E05 Inst. Pluviales", "Ejecución correspondiente a la partida E05 Inst. Pluviales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E05 Inst. Pluviales", "Ejecución correspondiente a la partida E05 Inst. Pluviales de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E06 Voz y Datos", "Ejecución correspondiente a la partida E06 Voz y Datos de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D09 Recubrim./Pint.", "Ejecución correspondiente a la partida D09 Recubrim./Pint. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E07 Recubrim./Pint.", "Ejecución correspondiente a la partida E07 Recubrim./Pint. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E07 Recubrim./Pint.", "Ejecución correspondiente a la partida E07 Recubrim./Pint. de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D10 Cancelería", "Ejecución correspondiente a la partida D10 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E08 Cancelería", "Ejecución correspondiente a la partida E08 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E08 Cancelería", "Ejecución correspondiente a la partida E08 Cancelería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D11 Lambrín WPC", "Ejecución correspondiente a la partida D11 Lambrín WPC de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E09 Lambrín WPC", "Ejecución correspondiente a la partida E09 Lambrín WPC de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E09 Lambrín WPC", "Ejecución correspondiente a la partida E09 Lambrín WPC de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D12 Herrería", "Ejecución correspondiente a la partida D12 Herrería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D12 Herrería", "Ejecución correspondiente a la partida D12 Herrería de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["D13 Limpieza", "Ejecución correspondiente a la partida D13 Limpieza de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
      ["E10 Limpieza", "Ejecución correspondiente a la partida E10 Limpieza de acuerdo con el catálogo de conceptos del presupuesto y especificaciones constructivas."],
    ]
  },
]

if __name__ == "__main__":
    # ── Read the template HTML ──────────────────────────────────────────────
    src = r"e:\NEGOCIO\GUADALAJARA\Learning Hero\Nueva carpeta\gantt_mobile.html"
    with open(src, encoding="utf-8") as f:
        html = f.read()

    # ── Build new projectData JS ───────────────────────────────────────────────
    def js_zone(z):
        tasks_js = json.dumps(z["tasks"], ensure_ascii=False)
        details_js = ",\n        ".join(
            f'{{title:{json.dumps(t, ensure_ascii=False)},desc:{json.dumps(d, ensure_ascii=False)}}}'
            for t,d in z["details"]
        )
        return (
            f'{{ zone:{json.dumps(z["zone"], ensure_ascii=False)}, emoji:{json.dumps(z["emoji"], ensure_ascii=False)},\n'
            f'      tasks:{tasks_js},\n'
            f'      details:[\n        {details_js}\n      ], progress:Array(32).fill(0) }}'
        )

    new_pd = "const projectData = [\n    " + ",\n    ".join(js_zone(z) for z in ZONES) + "\n];"

    # Replace projectData block (from const projectData to the closing ];)
    html = re.sub(r'const projectData = \[[\s\S]*?\];', new_pd, html)

    # ── Structural: 16 → 32 ────────────────────────────────────────────────────
    # Slider max
    html = html.replace('max="16" value="1"', 'max="32" value="1"')

    # JS loops and limits
    html = html.replace('for(let i=1;i<=16;i++)', 'for(let i=1;i<=32;i++)')
    html = html.replace('for(let i=1; i <= 16; i++)', 'for(let i=1; i <= 32; i++)')
    html = html.replace('for(let i=1;i\u003c=16;i++)', 'for(let i=1;i\u003c=32;i++)')  # HTML-escaped
    html = html.replace('/15*100', '/31*100')
    html = html.replace('16-currentWeek', '32-currentWeek')
    html = html.replace('currentWeek-1}/15', 'currentWeek-1}/31')
    # Stats text
    html = html.replace('5 zonas · 16 semanas', '5 zonas · 32 semanas')
    html = html.replace('Ampliación · 5 zonas · 16 semanas', 'Proyecto SAUCES · 5 zonas · 32 semanas')
    html = html.replace('Proyecto SAUCES · 5 zonas · 16 semanas', 'Proyecto SAUCES · 5 zonas · 32 semanas')
    # Gantt table width
    html = html.replace('min-width:800px', 'min-width:1600px')
    html = html.replace('min-width: 800px', 'min-width: 1600px')
    html = html.replace('min-width:900px', 'min-width:1600px')
    # Week pip grid columns
    html = html.replace('repeat(8, 1fr)', 'repeat(16, 1fr)')
    html = html.replace('repeat(8,1fr)', 'repeat(16,1fr)')

    # ── Write output ──────────────────────────────────────────────────────────
    with open(src, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ Gantt expandido a 32 semanas.")
    print(f"   Zonas: {len(ZONES)}")
    print(f"   Tareas por zona: 32")
    print(f"   Descripciones totales: {sum(len(z['details']) for z in ZONES)}")

