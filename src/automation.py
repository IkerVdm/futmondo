from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class DesktopAutomation:
    config: dict[str, Any]
    portfolio_path: Path
    dry_run: bool = False

    def log(self, message: str) -> None:
        prefix = "[dry-run]" if self.dry_run else "[run]"
        print(f"{prefix} {message}")

    def wait(self, seconds: float | None = None) -> None:
        delay = seconds if seconds is not None else float(
            self.config.get("default_pause_seconds", 0.5)
        )
        self.log(f"esperando {delay:.2f}s")
        if not self.dry_run:
            time.sleep(delay)

    def press(self, key: str) -> None:
        self.log(f"pulsando tecla '{key}'")
        if self.dry_run:
            return
        import pyautogui

        pyautogui.press(key)

    def click(self, x: int, y: int) -> None:
        self.log(f"clic en ({x}, {y})")
        if self.dry_run:
            return
        import pyautogui

        pyautogui.click(x=x, y=y)

    def click_named(self, point_name: str) -> None:
        points = self.config.get("ui", {}).get("click_points", {})
        if point_name not in points:
            raise KeyError(f"No existe el punto '{point_name}' en config.json")

        x, y = points[point_name]
        self.click(int(x), int(y))

    def hotkey_from_config(self, action_name: str) -> None:
        hotkeys = self.config.get("hotkeys", {})
        if action_name not in hotkeys:
            raise KeyError(f"No existe la hotkey '{action_name}' en config.json")
        self.press(str(hotkeys[action_name]))

    def require_live_execution(self, task_name: str) -> None:
        execution_mode = str(self.config.get("execution_mode", "plan"))
        require_confirm = bool(
            self.config.get("safety", {}).get("require_confirm_flag_for_live", True)
        )

        if self.dry_run:
            raise RuntimeError(
                f"La tarea {task_name} no se ejecuta en dry-run. Usa una tarea de plan."
            )

        if execution_mode != "live":
            raise RuntimeError(
                f"La tarea {task_name} requiere execution_mode=live en config.json."
            )

        if require_confirm:
            self.log(
                f"modo live habilitado para {task_name}; se recomienda probar antes las tareas de plan"
            )
