import asyncio
from typing import Dict, List, Optional
from attr import define
from example_publisher.providers.jupiter import Jupiter
from structlog import get_logger
from example_publisher.provider import Provider

from example_publisher.providers.coin_gecko import CoinGecko
from example_publisher.config import Config
from example_publisher.providers.pyth_replicator import PythReplicator
from example_publisher.pythd import Pythd, SubscriptionId


log = get_logger()

TRADING = "trading"


@define
class Product:
    symbol: str
    product_account: str
    price_account: str
    exponent: int
    subscription_id: Optional[SubscriptionId]

def _handle_task_result(task: asyncio.Task) -> None:
    try:
        task.result()
    except asyncio.CancelledError:
        pass  # Task cancellation should not be logged as an error.
    except Exception:  # pylint: disable=broad-except
        log.exception(f'Exception raised by task = {task}')
        exit(1)

class Publisher:
    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self._product_update_task: asyncio.Task | None = None

        if not getattr(self.config, self.config.provider_engine):
            raise ValueError(f"Missing {self.config.provider_engine} config")

        if self.config.provider_engine == "coin_gecko":
            self.provider = CoinGecko(config.coin_gecko)
        elif self.config.provider_engine == "pyth_replicator":
            self.provider: Provider = PythReplicator(config.pyth_replicator)
        elif self.config.provider_engine == "jupiter":
            self.provider: Provider = Jupiter(config.jupiter)
        else:
            raise ValueError(f"Unknown provider {self.config.provider_engine}")

        self.pythd: Pythd = Pythd(
            address=config.pythd.endpoint,
            on_notify_price_sched=self.on_notify_price_sched,
        )
        self.subscriptions: Dict[SubscriptionId, Product] = {}
        self.products: List[Product] = []

    async def start(self):
        await self.pythd.connect()

        self._product_update_task = asyncio.create_task(self._start_product_update_loop())

    async def _start_product_update_loop(self):
        await self._upd_products()
        provider_task = self.provider.start()
        provider_task.add_done_callback(_handle_task_result)

        while True:
            await self._upd_products()
            await self._subscribe_notify_price_sched()
            await asyncio.sleep(self.config.product_update_interval_secs)

    async def _upd_products(self):
        log.debug("fetching product accounts from Pythd")
        pythd_products = {
            product.metadata.symbol: product
            for product in await self.pythd.all_products()
        }
        log.debug("fetched product accounts from Pythd", products=pythd_products)

        old_products_by_symbol = {product.symbol: product for product in self.products}

        self.products = []

        for symbol, product in pythd_products.items():
            if not product.prices:
                continue

            subscription_id = None
            if old_product := old_products_by_symbol.get(symbol):
                subscription_id = old_product.subscription_id

            self.products.append(
                Product(
                    symbol,
                    product.account,
                    product.prices[0].account,
                    product.prices[0].exponent,
                    subscription_id,
                )
            )

        filtered_symbols = self.provider.upd_products([product.symbol for product in self.products])
        if filtered_symbols:
            self.products = list(filter(lambda p: p.symbol in filtered_symbols, self.products))


    async def _subscribe_notify_price_sched(self):
        # Subscribe to Pythd's notify_price_sched for each product that
        # is not subscribed yet. Unfortunately there is no way to unsubscribe
        # to the prices that are no longer available.
        log.debug("subscribing to notify_price_sched")

        subscriptions = {}
        for product in self.products:
            if not product.subscription_id:
                subscription_id = await self.pythd.subscribe_price_sched(
                    product.price_account
                )
                product.subscription_id = subscription_id

            subscriptions[product.subscription_id] = product

        self.subscriptions = subscriptions

    async def on_notify_price_sched(self, subscription: int) -> None:

        log.debug("received notify_price_sched", subscription=subscription)
        if subscription not in self.subscriptions:
            return

        # Look up the current price and confidence interval of the product
        product = self.subscriptions[subscription]
        price = self.provider.latest_price(product.symbol)
        if not price:
            log.info("latest price not available", symbol=product.symbol)
            return

        # Scale the price and confidence interval using the Pyth exponent
        scaled_price = self.apply_exponent(price.price, product.exponent)
        scaled_conf = self.apply_exponent(price.conf, product.exponent)

        # Send the price update
        log.info(
            "sending update_price",
            product_account=product.product_account,
            price_account=product.price_account,
            price=scaled_price,
            conf=scaled_conf,
            symbol=product.symbol,
        )
        await self.pythd.update_price(
            product.price_account, scaled_price, scaled_conf, TRADING
        )

    def apply_exponent(self, x: float, exp: int) -> int:
        return int(x * (10 ** (-exp)))
