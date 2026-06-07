from __future__ import annotations

from argparse import Namespace

from futmondo.automation import DesktopAutomation
from futmondo.market.models import ROLE_CORE, ROLE_HOLD, ROLE_TRADE
from futmondo.market.rules import build_buy_plan, build_sell_plan, compute_free_slots
from futmondo.market.storage import (
    load_portfolio,
    load_squad_snapshot,
    save_portfolio,
)
from futmondo.market.sync import merge_snapshot_into_portfolio


CURRENT_CORE_NAMES = {
    "Vinicius",
    "Oyarzabal",
    "Raphinha",
    "Moleiro",
    "Jauregizar",
    "Arambarri",
    "C. Soler",
    "Dela",
    "Pedraza",
    "A. Martinez",
    "Ryan",
    "Ugrinic",
    "J. Alvarez",
    "Comesana",
    "A. Ruibal",
}


def status_mercado(bot: DesktopAutomation, _: Namespace) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    free_slots = compute_free_slots(bot.config, portfolio)
    owned = [player for player in portfolio.players if player.status == "owned"]
    core = [player for player in owned if player.role == ROLE_CORE]
    trade = [player for player in owned if player.role == ROLE_TRADE]
    hold = [player for player in owned if player.role == ROLE_HOLD]
    bot.log(f"saldo={portfolio.balance}")
    bot.log(f"jugadores_en_propiedad={len(owned)}")
    bot.log(f"jugadores_core={len(core)}")
    bot.log(f"jugadores_trade={len(trade)}")
    bot.log(f"jugadores_hold={len(hold)}")
    bot.log(f"pujas_pendientes={len(portfolio.pending_bids)}")
    bot.log(f"huecos_libres={free_slots}")


def plan_ventas(bot: DesktopAutomation, _: Namespace) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    actions = build_sell_plan(bot.config, portfolio)
    if not actions:
        bot.log("sin ventas planificadas")
        return

    for action in actions:
        bot.log(
            f"plan venta jugador={action.player_name} motivo={action.reason} precio={action.amount}"
        )


def plan_compras(bot: DesktopAutomation, _: Namespace) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    actions = build_buy_plan(bot.config, portfolio)
    if not actions:
        bot.log("sin compras planificadas")
        return

    for action in actions:
        bot.log(
            f"plan compra jugador={action.player_name} motivo={action.reason} puja={action.amount}"
        )


def marcar_claves_actuales(bot: DesktopAutomation, _: Namespace) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    updated = 0
    for player in portfolio.players:
        if player.name in CURRENT_CORE_NAMES:
            player.role = ROLE_CORE
            player.allow_auto_sell = False
            updated += 1

    save_portfolio(bot.portfolio_path, portfolio)
    bot.log(f"jugadores_clave_actualizados={updated}")


def configurar_roles(bot: DesktopAutomation, _: Namespace) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    if not portfolio.players:
        bot.log("no hay jugadores en players.json para configurar")
        return

    bot.log("configuracion interactiva de roles iniciada")
    print("Opciones: core, trade, hold, skip")
    for player in sorted(portfolio.players, key=lambda item: item.name.lower()):
        current = player.role
        answer = input(f"{player.name} [{current}]: ").strip().lower()
        if not answer or answer == "skip":
            continue
        if answer == ROLE_CORE:
            player.role = ROLE_CORE
            player.allow_auto_sell = False
        elif answer == ROLE_TRADE:
            player.role = ROLE_TRADE
            player.allow_auto_sell = True
        elif answer == ROLE_HOLD:
            player.role = ROLE_HOLD
            player.allow_auto_sell = False
        else:
            print(f"Valor no valido para {player.name}, se mantiene {current}")

    save_portfolio(bot.portfolio_path, portfolio)
    bot.log("configuracion interactiva de roles guardada")


def revisar_roles_pendientes(bot: DesktopAutomation, _: Namespace) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    pending = sorted(
        [
            player.name
            for player in portfolio.players
            if player.status == "owned" and player.role == ROLE_HOLD
        ]
    )
    if not pending:
        bot.log("sin jugadores pendientes de revisar rol")
        return

    bot.log(f"roles_pendientes={len(pending)}")
    for name in pending:
        bot.log(f"revisar_rol jugador={name}")


def sincronizar_plantilla_desde_archivo(bot: DesktopAutomation, args: Namespace) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    snapshot = load_squad_snapshot(args.sync_source)
    result = merge_snapshot_into_portfolio(portfolio, snapshot)
    save_portfolio(bot.portfolio_path, portfolio)
    bot.log(
        "sincronizacion_guardada "
        f"altas={len(result.added_players)} "
        f"actualizados={len(result.updated_players)} "
        f"faltantes={len(result.missing_players)} "
        f"roles_pendientes={len(result.pending_role_review)}"
    )
    for name in result.pending_role_review:
        bot.log(f"revisar_rol jugador={name}")
    for name in result.missing_players:
        bot.log(f"jugador_no_detectado_en_sync jugador={name}")


def ejecutar_ventas(bot: DesktopAutomation, _: Namespace) -> None:
    bot.require_live_execution("ejecutar_ventas")
    portfolio = load_portfolio(bot.portfolio_path)
    actions = build_sell_plan(bot.config, portfolio)
    if not actions:
        bot.log("sin ventas a ejecutar")
        return

    bot.log("ejecucion limitada: solo lista ventas ya aprobadas por reglas")
    bot.click_named("market_tab_sell")
    bot.wait()
    for action in actions:
        bot.log(
            f"pendiente implementar seleccion visual de venta jugador={action.player_name} precio={action.amount}"
        )


def ejecutar_compras(bot: DesktopAutomation, _: Namespace) -> None:
    bot.require_live_execution("ejecutar_compras")
    portfolio = load_portfolio(bot.portfolio_path)
    actions = build_buy_plan(bot.config, portfolio)
    if not actions:
        bot.log("sin compras a ejecutar")
        return

    bot.log("ejecucion limitada: solo pujas aprobadas por reglas")
    bot.click_named("market_tab_buy")
    bot.wait()
    for action in actions:
        bot.log(
            f"pendiente implementar seleccion visual de compra jugador={action.player_name} puja={action.amount}"
        )


TASKS = {
    "status_mercado": status_mercado,
    "plan_ventas": plan_ventas,
    "plan_compras": plan_compras,
    "marcar_claves_actuales": marcar_claves_actuales,
    "configurar_roles": configurar_roles,
    "revisar_roles_pendientes": revisar_roles_pendientes,
    "sincronizar_plantilla_desde_archivo": sincronizar_plantilla_desde_archivo,
    "ejecutar_ventas": ejecutar_ventas,
    "ejecutar_compras": ejecutar_compras,
}
