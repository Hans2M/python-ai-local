# Diferencia entre conteo de eventos y conteo de usuarios

**Tema:** Sesión 12 — Análisis de registros de tráfico con Python  
**Nivel:** basico

Cada línea del CSV es un evento; una misma persona u origen puede producir múltiples eventos. Contar filas no revela necesariamente cuántas personas distintas participaron ni cuántas conexiones únicas existieron. Para contar entidades únicas haría falta un identificador o criterio adicional, que la clase no proporciona.
