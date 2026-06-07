from __future__ import annotations

from futmondo.lineups.tasks import TASKS as LINEUPS_TASKS
from futmondo.market.tasks import TASKS as MARKET_TASKS


TASKS = {
    **MARKET_TASKS,
    **LINEUPS_TASKS,
}
