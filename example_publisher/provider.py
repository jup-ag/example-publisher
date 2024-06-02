from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from typing import List, Optional

Symbol = str


@dataclass
class Price:
    price: float
    conf: float


class Provider(ABC):
    _update_loop_task = None

    @abstractmethod
    def upd_products(self, product_symbols: List[Symbol]) -> List[Symbol] | None:
        ...

    def start(self) -> asyncio.Task:
        self._update_loop_task = asyncio.create_task(self._update_loop())
        return self._update_loop_task

    @abstractmethod
    async def _update_loop(self):
        ...

    @abstractmethod
    def latest_price(self, symbol: Symbol) -> Optional[Price]:
        ...
