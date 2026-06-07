from __future__ import annotations

from argparse import Namespace

from futmondo.automation import DesktopAutomation


def estado_lineups(bot: DesktopAutomation, _: Namespace) -> None:
    bot.log("lineups_modulo_preparado estado=pendiente_de_implementar")
    bot.log("siguiente_hito=validacion_previa_jornada_y_guardado_de_alineacion")


TASKS = {
    "estado_lineups": estado_lineups,
}
