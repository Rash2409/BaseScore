import random
import time
import asyncio

from loguru import logger
from utils.db_api.models import Wallet
from withdrawal.okx_actions import OKXActions
from libs.py_okx_async.models import Chains
from libs.eth_async.client import Client
from libs.eth_async.data.models import Networks
from libs.eth_async.utils.utils import randfloat

from data.models import Settings


async def okx_withdraw_to_base(wallets: list[Wallet]):
    settings = Settings()
    okx = OKXActions(credentials=settings.okx.credentials)

    for num, wallet in enumerate(wallets, start=1):
        logger.info(f'{num}/{len(wallets)} wallets')

        client = Client(private_key=wallet.private_key, network=Networks.Base, proxy=wallet.proxy)

        amount_to_withdraw = randfloat(
            from_=settings.okx.withdraw_amount.from_,
            to_=settings.okx.withdraw_amount.to_,
            step=0.0001
        )

        res = await okx.withdraw(
            to_address=str(client.account.address),
            amount=amount_to_withdraw,
            token_symbol='ETH',
            chain=Chains.Base
        )

        if 'Failed' not in res:
            logger.success(f'{wallet.address}: {res} | Base')
            if num >= len(wallets):
                logger.success(f'OKX withdraw to Base successfully completed with {len(wallets)} wallets')
                return

            time.sleep(random.randint(
                settings.okx.delay_between_withdrawals.from_, settings.okx.delay_between_withdrawals.to_))
        else:
            logger.error(f'{wallet.address}: {res}')
