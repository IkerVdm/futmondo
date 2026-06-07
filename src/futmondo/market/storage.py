from __future__ import annotations

import json
from pathlib import Path

from futmondo.market.models import (
    BuyTarget,
    PendingBid,
    Player,
    Portfolio,
    SquadSnapshot,
    SquadSnapshotPlayer,
    normalize_role,
)


def _load_json(path: Path | str, example_hint: str) -> dict:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"No existe {path}. Crea el archivo copiando {example_hint}.")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_portfolio(path: Path | str) -> Portfolio:
    raw = _load_json(path, "data/players.example.json")

    players: list[Player] = []
    for item in raw.get("players", []):
        player = Player(**item)
        player.role = normalize_role(player.role)
        if player.role != "trade":
            player.allow_auto_sell = False
        players.append(player)

    return Portfolio(
        balance=int(raw.get("balance", 0)),
        players=players,
        buy_targets=[BuyTarget(**item) for item in raw.get("buy_targets", [])],
        pending_bids=[PendingBid(**item) for item in raw.get("pending_bids", [])],
    )


def load_squad_snapshot(path: Path | str) -> SquadSnapshot:
    raw = _load_json(path, "data/squad_sync.example.json")
    return SquadSnapshot(
        balance=int(raw.get("balance", 0)),
        players=[SquadSnapshotPlayer(**item) for item in raw.get("players", [])],
        pending_bids=[PendingBid(**item) for item in raw.get("pending_bids", [])],
    )


def save_portfolio(path: Path | str, portfolio: Portfolio) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "balance": portfolio.balance,
        "players": [
            {
                "name": player.name,
                "role": normalize_role(player.role),
                "status": player.status,
                "buy_price": player.buy_price,
                "current_value": player.current_value,
                "allow_auto_sell": player.allow_auto_sell and normalize_role(player.role) == "trade",
                "target_profit_pct": player.target_profit_pct,
                "stop_loss_pct": player.stop_loss_pct,
            }
            for player in portfolio.players
        ],
        "buy_targets": [
            {
                "name": target.name,
                "max_bid": target.max_bid,
                "priority": target.priority,
                "enabled": target.enabled,
            }
            for target in portfolio.buy_targets
        ],
        "pending_bids": [
            {
                "name": bid.name,
                "amount": bid.amount,
            }
            for bid in portfolio.pending_bids
        ],
    }
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=True, indent=2)
        file.write("\n")
