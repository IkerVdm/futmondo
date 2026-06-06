from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Player:
    name: str
    role: str
    status: str
    buy_price: int = 0
    current_value: int = 0
    allow_auto_sell: bool = False
    target_profit_pct: float | None = None
    stop_loss_pct: float | None = None

    @property
    def profit_pct(self) -> float:
        if self.buy_price <= 0:
            return 0.0
        return (self.current_value - self.buy_price) / self.buy_price


@dataclass
class BuyTarget:
    name: str
    max_bid: int
    priority: int = 100
    enabled: bool = True


@dataclass
class PendingBid:
    name: str
    amount: int


@dataclass
class Portfolio:
    balance: int
    players: list[Player] = field(default_factory=list)
    buy_targets: list[BuyTarget] = field(default_factory=list)
    pending_bids: list[PendingBid] = field(default_factory=list)


@dataclass
class PlannedAction:
    action: str
    player_name: str
    reason: str
    amount: int | None = None
