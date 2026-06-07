from __future__ import annotations

import argparse
import json
from pathlib import Path

from futmondo.automation import DesktopAutomation
from futmondo.tasks import TASKS


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / "config.json"
DEFAULT_PORTFOLIO_PATH = BASE_DIR / "data" / "players.json"
DEFAULT_SYNC_SOURCE_PATH = BASE_DIR / "data" / "squad_sync.json"


def load_json_file(path: Path, example_hint: str) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"No existe {path}. Crea el archivo copiando {example_hint}.")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI modular para automatizar tareas de Futmondo."
    )
    parser.add_argument("--task", help="Nombre de la tarea a ejecutar.")
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Ruta al archivo config.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula pasos sin pulsar teclas ni mover el raton.",
    )
    parser.add_argument(
        "--portfolio",
        default=str(DEFAULT_PORTFOLIO_PATH),
        help="Ruta al archivo con plantilla, objetivos y pujas.",
    )
    parser.add_argument(
        "--sync-source",
        default=str(DEFAULT_SYNC_SOURCE_PATH),
        help="Ruta al snapshot local para sincronizar plantilla real.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lista las tareas disponibles.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        print("Tareas disponibles:")
        for task_name in TASKS:
            print(f"- {task_name}")
        return 0

    if not args.task:
        parser.error("Debes indicar --task o usar --list.")

    if args.task not in TASKS:
        available = ", ".join(TASKS)
        parser.error(f"Tarea desconocida: {args.task}. Disponibles: {available}")

    config = load_json_file(Path(args.config), "config.example.json")
    bot = DesktopAutomation(
        config=config,
        portfolio_path=Path(args.portfolio),
        dry_run=args.dry_run,
    )
    TASKS[args.task](bot, args)
    return 0
