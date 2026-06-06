from __future__ import annotations

import json
from pathlib import Path

from futmondo_models import BuyTarget, PendingBid, Player, Portfolio


def load_portfolio(path: Path) -> Portfolio:
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Crea el archivo copiando data/players.example.json."
        )

    with path.open("r", encoding="utf-8") as file:
        raw = json.load(file)

    return Portfolio(
        balance=int(raw.get("balance", 0)),
        players=[Player(**item) for item in raw.get("players", [])],
        buy_targets=[BuyTarget(**item) for item in raw.get("buy_targets", [])],
        pending_bids=[PendingBid(**item) for item in raw.get("pending_bids", [])],
    )


def save_portfolio(path: Path, portfolio: Portfolio) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "balance": portfolio.balance,
        "players": [
            {
                "name": player.name,
                "role": player.role,
                "status": player.status,
                "buy_price": player.buy_price,
                "current_value": player.current_value,
                "allow_auto_sell": player.allow_auto_sell,
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
