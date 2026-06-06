from __future__ import annotations

from automation import DesktopAutomation


def recoger_recompensa(bot: DesktopAutomation) -> None:
    bot.log("iniciando tarea recoger_recompensa")
    bot.hotkey_from_config("abrir_menu")
    bot.wait()
    bot.click_named("recompensa_diaria")
    bot.wait(1.0)
    bot.hotkey_from_config("confirmar")
    bot.wait()
    bot.click_named("cerrar_popup")
    bot.log("tarea completar recoger_recompensa")


def bucle_base(bot: DesktopAutomation) -> None:
    total = int(bot.config.get("loops", {}).get("repeticiones_base", 3))
    bot.log(f"iniciando bucle_base con {total} repeticiones")

    for index in range(total):
        bot.log(f"iteracion {index + 1}/{total}")
        bot.hotkey_from_config("abrir_menu")
        bot.wait()
        bot.hotkey_from_config("confirmar")
        bot.wait()

    bot.log("tarea completar bucle_base")


TASKS = {
    "recoger_recompensa": recoger_recompensa,
    "bucle_base": bucle_base,
}
