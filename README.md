# Futmondo

Proyecto base para automatizar Futmondo por modulos. La primera fase cubre mercado y pruebas controladas de compra/venta; despues se podran anadir alineaciones, validaciones previas a jornada y mas reglas de negocio.

La idea es simple:

- Definir tareas repetitivas como secuencias de pasos.
- Mantener posiciones, pausas y atajos en un archivo de configuracion.
- Poder probar todo en modo seguro con `--dry-run` antes de mover raton o pulsar teclas.

## Estructura

- `requirements.txt`: dependencias recomendadas.
- `config.example.json`: configuracion del campeonato y seguridad.
- `data/players.example.json`: plantilla, objetivos de compra y pujas pendientes.
- `src/main.py`: punto de entrada.
- `src/automation.py`: capa de automatizacion.
- `src/futmondo_*.py`: reglas y tareas de Futmondo.
- `ROADMAP.md`: plan del proyecto global.

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
```

## Uso

Ver tareas disponibles:

```powershell
python .\src\main.py --list
python .\src\main.py --task status_mercado --dry-run
```

Marcar como `core` los jugadores clave actuales:

```powershell
python .\src\main.py --task marcar_claves_actuales --dry-run
```

Configurar roles de forma interactiva cuando cambie tu plantilla:

```powershell
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

1. Rellena `data/players.json` con tu plantilla real.
2. Marca cada jugador como `core` o `trade`.
3. Añade objetivos en `buy_targets`.
4. Ejecuta primero `status_mercado`, `plan_ventas` y `plan_compras`.
5. Solo cuando el plan sea correcto, activa `execution_mode: "live"`.

Los jugadores `core` actuales detectados desde tu captura son:

- `Vinicius`
- `Oyarzabal`
- `Raphinha`
- `Moleiro`
- `Jauregizar`
- `Arambarri`
- `C. Soler`
- `Dela`
- `Pedraza`
- `A. Martinez`
- `Ryan`
- `Ugrinic`
- `J. Alvarez`
- `Comesana`
- `A. Ruibal`

## Como adaptar las tareas

Edita `src/futmondo_tasks.py`. Cada tarea es una funcion que recibe una instancia de `DesktopAutomation`.

Ejemplo de cosas tipicas que puedes automatizar:

- Sincronizar plantilla.
- Planificar ventas de jugadores `trade`.
- Planificar compras con limite de plazas.
- Revisar pujas pendientes.
- Ejecutar compras y ventas solo en modo `live`.

## Siguiente paso util

Cuando tengas tu plantilla y objetivos reales, la mejor mejora es capturar coordenadas reales de Futmondo y reemplazar los logs de `ejecutar_ventas` y `ejecutar_compras` por interacciones visuales concretas.

## Git

El proyecto ya puede vivir como repo independiente `futmondo`.

Archivos locales sensibles que no deben subirse:

- `config.json`
- `data/players.json`
- sesiones o credenciales futuras
