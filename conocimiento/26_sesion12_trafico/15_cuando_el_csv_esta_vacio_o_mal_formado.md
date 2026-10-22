# Cuando el CSV esta vacio o mal formado

**Tema:** Sesión 12 — Análisis de registros de tráfico con Python  
**Nivel:** basico

Un archivo con solo encabezados produce cero eventos y cero bytes y contadores vacíos. Si un registro trae bytes vacíos o no numéricos, int() fallará: informar el dato problemático en vez de inventar una suma. Son validaciones adicionales; para un ejercicio básico de sesión 12 se puede asumir el CSV de práctica correctamente formado.
