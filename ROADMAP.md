# Futmondo Roadmap

Proyecto global para automatizar tareas de Futmondo por modulos.

## Modulos

- `market`: compra, venta, pujas, control de plazas y cartera `core/trade`.
- `lineups`: alineaciones, validacion previa a jornada y guardado.
- `watchlist`: objetivos de fichaje, prioridad y limites de puja.
- `reporting`: estado de cartera, logs y decisiones tomadas.
- `orchestration`: integracion con OpenClaw para cronjobs y ejecuciones programadas.

## Fases

1. `market-v1`
   - cartera local
   - roles `core/trade/hold`
   - plan de compras
   - plan de ventas
   - seguridad por modo `plan/live`
2. `market-v2`
   - sincronizacion real con Futmondo
   - ejecucion visual de pujas y ventas
   - control de errores de UI
3. `lineups-v1`
   - catalogo de jugadores alineables
   - guardado de alineaciones
   - comprobacion de posiciones y huecos
4. `decision-layer`
   - reglas de negocio mas finas
   - stop loss
   - take profit
   - prioridades por jornada

## Regla de arquitectura

Cada tarea automatizable debe existir como accion aislada y poder ejecutarse sola desde CLI.
