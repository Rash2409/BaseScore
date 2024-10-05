import asyncio

from loguru import logger

from functions.create_files import create_files
from functions.Import import Import
from data.models import Settings
from utils.db_api.wallet_api import get_wallets
from utils.db_api.models import Wallet
from withdrawal.main import okx_withdraw
from withdrawal.main2 import okx_withdraw_to_base
from withdrawal.main3 import okx_withdraw_to_arb
from functions.initial import initial


async def start_script():
    await asyncio.wait([asyncio.create_task(initial())])


async def start_okx_withdraw():
    settings = Settings()
    if not settings.okx.credentials.completely_filled():
        logger.error('OKX credentials not filled')
        return
    wallets: list[Wallet] = get_wallets()
    await okx_withdraw(wallets=wallets)


async def start_okx_withdraw_to_base():
    settings = Settings()
    if not settings.okx.credentials.completely_filled():
        logger.error('OKX credentials not filled')
        return
    wallets: list[Wallet] = get_wallets()
    await okx_withdraw_to_base(wallets=wallets)


async def start_okx_withdraw_to_arb():
    settings = Settings()
    if not settings.okx.credentials.completely_filled():
        logger.error('OKX credentials not filled')
        return
    wallets: list[Wallet] = get_wallets()
    await okx_withdraw_to_arb(wallets=wallets)


if __name__ == '__main__':
    create_files()
    print('''  Select the action:
1) Import wallets from the spreadsheet to the DB;
2) Start the script;
3) Start withdraw ETH from OKX(BASE | ARB)
4) Start withdraw ETH from OKX(BASE)
5) Start withdraw ETH from OKX(ARB)
6) Exit.''')

    try:
        action = int(input('> '))
        if action == 1:
            asyncio.run(Import.wallets())

        elif action == 2:
            asyncio.run(start_script())

        elif action == 3:
            asyncio.run(start_okx_withdraw())

        elif action == 4:
            asyncio.run(start_okx_withdraw_to_base())

        elif action == 5:
            asyncio.run(start_okx_withdraw_to_arb())

    except KeyboardInterrupt:
        print()

    except ValueError as err:
        logger.error(f'Value error: {err}')

    except BaseException as e:
        logger.error(f'Something went wrong: {e}')
