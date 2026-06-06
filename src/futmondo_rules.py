from __future__ import annotations

from futmondo_models import PlannedAction, Portfolio


def compute_free_slots(config: dict, portfolio: Portfolio) -> int:
    max_squad_size = int(config["league"]["max_squad_size"])
    owned_players = len([player for player in portfolio.players if player.status == "owned"])
    pending_bids = len(portfolio.pending_bids)
    consumed_slots = owned_players
    if config["league"].get("count_pending_bids_as_slots", True):
        consumed_slots += pending_bids
    return max(0, max_squad_size - consumed_slots)


def build_sell_plan(config: dict, portfolio: Portfolio) -> list[PlannedAction]:
    default_target = float(config["strategy"]["default_target_profit_pct"])
    default_stop_loss = float(config["strategy"]["default_stop_loss_pct"])
    actions: list[PlannedAction] = []

    for player in portfolio.players:
        if player.status != "owned":
            continue
        if player.role != "trade":
            continue
        if not player.allow_auto_sell:
            continue

        target_profit = (
            player.target_profit_pct
            if player.target_profit_pct is not None
            else default_target
        )
        stop_loss = (
            player.stop_loss_pct if player.stop_loss_pct is not None else default_stop_loss
        )

        if player.profit_pct >= target_profit:
            actions.append(
                PlannedAction(
                    action="sell",
                    player_name=player.name,
                    reason=f"target_profit_reached:{player.profit_pct:.2%}",
                    amount=player.current_value,
                )
            )
            continue

        if player.profit_pct <= stop_loss:
            actions.append(
                PlannedAction(
                    action="sell",
                    player_name=player.name,
                    reason=f"stop_loss_triggered:{player.profit_pct:.2%}",
                    amount=player.current_value,
                )
            )

    return actions


def build_buy_plan(config: dict, portfolio: Portfolio) -> list[PlannedAction]:
    reserve_cash = int(config["strategy"]["reserve_cash"])
    free_slots = compute_free_slots(config, portfolio)
    available_cash = max(0, portfolio.balance - reserve_cash)
    actions: list[PlannedAction] = []

    if free_slots <= 0 or available_cash <= 0:
        return actions

    sorted_targets = sorted(
        [target for target in portfolio.buy_targets if target.enabled],
        key=lambda item: item.priority,
    )
    pending_names = {bid.name for bid in portfolio.pending_bids}
    owned_names = {player.name for player in portfolio.players if player.status == "owned"}

    for target in sorted_targets:
        if free_slots <= 0:
            break
        if target.name in pending_names or target.name in owned_names:
            continue
        if target.max_bid > available_cash:
            continue

        actions.append(
            PlannedAction(
                action="bid",
                player_name=target.name,
                reason="buy_target_enabled",
                amount=target.max_bid,
            )
        )
        free_slots -= 1
        available_cash -= target.max_bid

    return actions
