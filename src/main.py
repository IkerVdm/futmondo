from __future__ import annotations

import argparse
import json
from pathlib import Path

from automation import DesktopAutomation
from futmondo_tasks import TASKS


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / "config.json"
DEFAULT_PORTFOLIO_PATH = BASE_DIR / "data" / "players.json"


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        raise FileNotFoundError(
            f"No existe {config_path}. Crea el archivo copiando config.example.json."
        )

    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automatizacion basica para tareas repetitivas en OpenClaw."
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

    config = load_config(Path(args.config))
    bot = DesktopAutomation(
        config=config,
        portfolio_path=Path(args.portfolio),
        dry_run=args.dry_run,
    )
    TASKS[args.task](bot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
