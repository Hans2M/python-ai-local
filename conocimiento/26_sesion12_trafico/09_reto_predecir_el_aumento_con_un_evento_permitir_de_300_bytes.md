# Reto: predecir el aumento con un evento PERMITIR de 300 bytes

**Tema:** Sesión 12 — Análisis de registros de tráfico con Python  
**Nivel:** basico

Si se añade UNA fila válida con accion PERMITIR y bytes 300, el número de eventos aumenta en 1, los bytes en 300 y el conteo PERMITIR aumenta en 1. También aumenta en 1 el contador del origen indicado en esa nueva fila; si se cuenta por servicio, también el servicio de la fila. Si la guía parte de 99 y 142690, la nueva salida sería 100 y 142990, suponiendo que la única modificación sea esa fila.
