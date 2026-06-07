# OpenClaw Integration

Esta guia define como debe usar OpenClaw este repositorio como base de automatizacion de Futmondo.

## Repositorio base

- GitHub: `https://github.com/IkerVdm/futmondo`
- Git clone: `https://github.com/IkerVdm/futmondo.git`
- Rama principal: `main`
- README: `https://github.com/IkerVdm/futmondo/blob/main/README.md`

## Regla principal

Cuando OpenClaw tenga que ir al mercado a comprar o vender en Futmondo, debe usar este script y estos comandos CLI. No debe inventar un flujo alternativo ni ejecutar compras o ventas fuera de este repositorio.

Punto de entrada:

```powershell
python .\src\main.py --task <nombre_tarea>
```

## Flujo obligatorio para mercado

1. Sincronizar plantilla real desde snapshot local.
2. Revisar jugadores con rol pendiente.
3. Planificar estado, ventas y compras en modo seguro.
4. Solo si el plan es correcto y `execution_mode` esta en `live`, ejecutar compras o ventas.

## Comandos que OpenClaw debe usar

Sincronizacion y revision:

```powershell
python .\src\main.py --task sincronizar_plantilla_desde_archivo --sync-source .\data\squad_sync.json
python .\src\main.py --task revisar_roles_pendientes
```

Planificacion segura:

```powershell
python .\src\main.py --task status_mercado --dry-run
python .\src\main.py --task plan_ventas --dry-run
python .\src\main.py --task plan_compras --dry-run
```

Ejecucion real solo si procede:

```powershell
python .\src\main.py --task ejecutar_ventas
python .\src\main.py --task ejecutar_compras
```

## Reglas que OpenClaw debe respetar

- por defecto, nada en modo peligroso
- primero planificar, luego ejecutar
- no vender automaticamente jugadores `core`
- separar jugadores `core`, `trade` y `hold`
- contar pujas pendientes como plazas consumidas si aplica
- mantener `config.json`, `data/players.json` y `data/squad_sync.json` fuera del repo
- si hay roles `hold`, OpenClaw debe pedir revision humana antes de asumir cambios importantes

## Cron jobs recomendados

Revision periodica de mercado:

```text
sincronizar_plantilla_desde_archivo -> revisar_roles_pendientes -> status_mercado -> plan_ventas -> plan_compras
```

Ejecucion real de mercado:

```text
solo despues de una planificacion correcta y solo con execution_mode=live
```

## Salida esperada para OpenClaw

OpenClaw debe leer los logs de consola de cada tarea y usarlos como base de decision.

Senales utiles actuales:

- `sincronizacion_guardada`
- `revisar_rol jugador=<nombre>`
- `plan venta jugador=<nombre>`
- `plan compra jugador=<nombre>`
- `sin ventas planificadas`
- `sin compras planificadas`

## Limite actual

La ejecucion visual real de `ejecutar_ventas` y `ejecutar_compras` todavia esta en modo base: entra en la pestana correcta y deja trazado lo pendiente de implementar para la seleccion visual fina. OpenClaw debe usar ya estos comandos como interfaz estable, aunque la capa visual todavia se pueda mejorar.
