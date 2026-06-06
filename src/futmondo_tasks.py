from __future__ import annotations

from futmondo_portfolio import load_portfolio, save_portfolio
from futmondo_rules import build_buy_plan, build_sell_plan, compute_free_slots
from automation import DesktopAutomation


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


def status_mercado(bot: DesktopAutomation) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    free_slots = compute_free_slots(bot.config, portfolio)
    bot.log(f"saldo={portfolio.balance}")
    bot.log(f"jugadores_en_propiedad={len(portfolio.players)}")
    bot.log(f"pujas_pendientes={len(portfolio.pending_bids)}")
    bot.log(f"huecos_libres={free_slots}")


def plan_ventas(bot: DesktopAutomation) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    actions = build_sell_plan(bot.config, portfolio)
    if not actions:
        bot.log("sin ventas planificadas")
        return

    for action in actions:
        bot.log(
            f"plan venta jugador={action.player_name} motivo={action.reason} precio={action.amount}"
        )


def plan_compras(bot: DesktopAutomation) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    actions = build_buy_plan(bot.config, portfolio)
    if not actions:
        bot.log("sin compras planificadas")
        return

    for action in actions:
        bot.log(
            f"plan compra jugador={action.player_name} motivo={action.reason} puja={action.amount}"
        )


def marcar_claves_actuales(bot: DesktopAutomation) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    updated = 0
    for player in portfolio.players:
        if player.name in CURRENT_CORE_NAMES:
            player.role = "core"
            player.allow_auto_sell = False
            updated += 1

    save_portfolio(bot.portfolio_path, portfolio)
    bot.log(f"jugadores_clave_actualizados={updated}")


def configurar_roles(bot: DesktopAutomation) -> None:
    portfolio = load_portfolio(bot.portfolio_path)
    if not portfolio.players:
        bot.log("no hay jugadores en players.json para configurar")
        return

    bot.log("configuracion interactiva de roles iniciada")
    print("Opciones: core, trade, hold, skip")
    for player in portfolio.players:
        current = player.role
        answer = input(f"{player.name} [{current}]: ").strip().lower()
        if not answer or answer == "skip":
            continue
        if answer == "core":
            player.role = "core"
            player.allow_auto_sell = False
        elif answer == "trade":
            player.role = "trade"
            player.allow_auto_sell = True
        elif answer == "hold":
            player.role = "manual_hold"
            player.allow_auto_sell = False
        else:
            print(f"Valor no valido para {player.name}, se mantiene {current}")

    save_portfolio(bot.portfolio_path, portfolio)
    bot.log("configuracion interactiva de roles guardada")


def ejecutar_ventas(bot: DesktopAutomation) -> None:
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


def ejecutar_compras(bot: DesktopAutomation) -> None:
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
    "ejecutar_ventas": ejecutar_ventas,
    "ejecutar_compras": ejecutar_compras,
}
