from __future__ import annotations

from dataclasses import dataclass

from futmondo.market.models import (
    PendingBid,
    Player,
    Portfolio,
    ROLE_HOLD,
    ROLE_TRADE,
    SquadSnapshot,
    normalize_role,
)


@dataclass
class SyncResult:
    added_players: list[str]
    updated_players: list[str]
    missing_players: list[str]
    pending_role_review: list[str]


def merge_snapshot_into_portfolio(
    portfolio: Portfolio,
    snapshot: SquadSnapshot,
) -> SyncResult:
    existing_by_name = {player.name: player for player in portfolio.players}
    snapshot_names = {player.name for player in snapshot.players}
    added_players: list[str] = []
    updated_players: list[str] = []
    pending_role_review: list[str] = []

    for source in snapshot.players:
        existing = existing_by_name.get(source.name)
        if existing is None:
            existing = Player(
                name=source.name,
                role=ROLE_HOLD,
                status=source.status,
                buy_price=source.buy_price,
                current_value=source.current_value,
                allow_auto_sell=False,
            )
            portfolio.players.append(existing)
            existing_by_name[source.name] = existing
            added_players.append(source.name)
            pending_role_review.append(source.name)
            continue

        existing.status = source.status
        existing.current_value = source.current_value
        if source.buy_price > 0:
            existing.buy_price = source.buy_price
        existing.role = normalize_role(existing.role)
        existing.allow_auto_sell = existing.role == ROLE_TRADE and existing.allow_auto_sell
        updated_players.append(source.name)
        if existing.role == ROLE_HOLD:
            pending_role_review.append(source.name)

    missing_players: list[str] = []
    for player in portfolio.players:
        if player.name not in snapshot_names and player.status == "owned":
            player.status = "missing_from_sync"
            player.role = normalize_role(player.role)
            player.allow_auto_sell = player.role == ROLE_TRADE and player.allow_auto_sell
            missing_players.append(player.name)

    portfolio.balance = snapshot.balance
    portfolio.pending_bids = [
        PendingBid(name=bid.name, amount=bid.amount) for bid in snapshot.pending_bids
    ]

    return SyncResult(
        added_players=sorted(added_players),
        updated_players=sorted(updated_players),
        missing_players=sorted(missing_players),
        pending_role_review=sorted(set(pending_role_review)),
    )
