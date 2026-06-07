# Futmondo

Base modular para automatizar Futmondo por tareas pequenas. La fase actual esta centrada en `market`: compras, ventas, pujas, control de plazas y separacion clara entre jugadores `core`, `trade` y `hold`.

Principios del proyecto:

- nada peligroso por defecto
- primero planificar, luego ejecutar
- no vender automaticamente jugadores `core`
- contar pujas pendientes como plazas consumidas si aplica
- separar configuracion y datos sensibles del repo

## Estructura

- `requirements.txt`: dependencias recomendadas para automatizacion visual.
- `config.example.json`: configuracion del campeonato y seguridad.
- `data/players.example.json`: cartera persistente con roles, objetivos y pujas.
- `data/squad_sync.example.json`: snapshot local para sincronizar tu plantilla real.
- `OPENCLAW.md`: instrucciones para que OpenClaw use este repo y sus tareas.
- `src/main.py`: punto de entrada de la CLI.
- `src/futmondo/market/`: reglas, almacenamiento, sincronizacion y tareas de mercado.
- `src/futmondo/lineups/`: modulo preparado para la siguiente fase.
- `ROADMAP.md`: plan global del proyecto.

## Requisitos

- Windows
- Python 3.10 o superior

## Instalacion

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item config.example.json config.json
New-Item -ItemType Directory .\data -Force
Copy-Item .\data\players.example.json .\data\players.json
Copy-Item .\data\squad_sync.example.json .\data\squad_sync.json
```

## Uso

Ver tareas disponibles:

```powershell
python .\src\main.py --list
python .\src\main.py --task status_mercado --dry-run
```

Sincronizar plantilla real y revisar roles:

```powershell
python .\src\main.py --task sincronizar_plantilla_desde_archivo --sync-source .\data\squad_sync.json
python .\src\main.py --task revisar_roles_pendientes
python .\src\main.py --task configurar_roles
```

Planificar ventas:

```powershell
python .\src\main.py --task plan_ventas --dry-run
```

Planificar compras:

```powershell
python .\src\main.py --task plan_compras --dry-run
```

Activar ejecucion real de forma explicita:

```powershell
# Cambia execution_mode a "live" en config.json
python .\src\main.py --task ejecutar_ventas
```

## Flujo recomendado

1. Rellena `data/players.json` con tu cartera base y objetivos.
2. Actualiza `data/squad_sync.json` con un snapshot real de plantilla, valores y pujas.
3. Ejecuta `sincronizar_plantilla_desde_archivo`.
4. Revisa `revisar_roles_pendientes` y ajusta `configurar_roles`.
5. Ejecuta `status_mercado`, `plan_ventas` y `plan_compras`.
6. Solo cuando el plan sea correcto, activa `execution_mode: "live"`.

## Tareas actuales de mercado

- `status_mercado`: resumen de saldo, plazas y composicion `core/trade/hold`.
- `plan_ventas`: solo propone ventas de jugadores `trade` con auto-sell permitido.
- `plan_compras`: genera pujas segun saldo util, plazas libres y prioridades.
- `sincronizar_plantilla_desde_archivo`: fusiona un snapshot real dentro de `players.json`.
- `revisar_roles_pendientes`: lista jugadores sincronizados que siguen en `hold`.
- `configurar_roles`: actualiza roles de forma interactiva.
- `ejecutar_ventas` y `ejecutar_compras`: reservadas para modo `live`.

## Como adaptar las tareas

Edita `src/futmondo/market/tasks.py` o anade nuevas acciones en un modulo especifico. Cada tarea debe existir como comando aislado y poder ejecutarse sola desde CLI.

## Siguiente paso util

Cuando el flujo de sincronizacion te funcione con datos reales, el siguiente paso natural es conectar la captura del snapshot con Futmondo y despues implementar `lineups` con validaciones previas a jornada.

## Git

Archivos locales sensibles que no deben subirse:

- `config.json`
- `data/players.json`
- `data/squad_sync.json`
- sesiones o credenciales futuras
