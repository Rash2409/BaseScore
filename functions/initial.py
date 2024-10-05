import random
import asyncio
from datetime import datetime, timedelta

from web3 import Web3
from loguru import logger

from libs.eth_async.client import Client
from libs.eth_async.data.models import Networks, TokenAmount
from tasks.base import randfloat

from data.models import Settings
from utils.db_api.wallet_api import db
from utils.db_api.models import Wallet
from tasks.controller import Controller
from functions.select_randon_action_new import select_random_action
from utils.update_expired import update_expired


async def initial():
    settings = Settings()

    delay = 20

    update_expired(initial=True)
    await asyncio.sleep(5)

    while True:
        try:
            now = datetime.now()

            wallet: Wallet = db.one(
                Wallet, Wallet.initial_completed.is_(False) & (Wallet.next_initial_action_time <= now)
            )

            if not wallet:
                await asyncio.sleep(delay)
                continue

            client = Client(private_key='', network=Networks.Base, proxy=wallet.proxy)

            gas_price = await client.transactions.gas_price()

            while float(gas_price.Wei) > Web3.to_wei(settings.maximum_gas_price, 'gwei'):
                logger.debug(f'Gas price is too hight '
                             f'({Web3.from_wei(gas_price.Wei, "gwei")} > {settings.maximum_gas_price})')
                await asyncio.sleep(60 * 1)
                gas_price = await client.transactions.gas_price()

            client = Client(private_key=wallet.private_key, network=Networks.Base, proxy=wallet.proxy)
            controller = Controller(client=client)

            client2 = Client(private_key=wallet.private_key, network=Networks.Arbitrum, proxy=wallet.proxy)
            controller2 = Controller(client=client2)

            now = datetime.now()

            action = await select_random_action(controller=controller, controller2=controller2, wallet=wallet)

            if not action:
                logger.error(f'{wallet.address} | select_random_action | can not choose the action')
                continue

            if action == 'Processed':
                wallet.initial_completed = True
                wallet.completed = True

                db.commit()
                logger.success(
                    f'{wallet.address}: initial actions completed!'
                )
                continue

            if action == 'Insufficient balance':
                logger.error(f'{wallet.address}: Недостаточно баланса, пополните кошелек')
                continue

            if action.__name__.startswith(
                    ('eth_to_usdc', 'eth_to_dai', 'eth_to_usdbc', 'eth_to_axlusdc')):
                status = await action(
                    amount=TokenAmount(
                        randfloat(
                            from_=settings.eth_amount_for_swap.from_,
                            to_=settings.eth_amount_for_swap.to_,
                            step=0.0001,
                        )
                    )
                )

            elif action.__name__.startswith(('axlusdc_to_eth', 'usdc_to_eth', 'dai_to_eth', 'usdbc_to_eth')):
                status = await action()

            elif action.__name__.startswith('depozit_eth'):
                status = await action(amount=TokenAmount(wallet.eth_amount_for_aave))

            elif action.__name__.startswith('withdraw_eth'):
                status = await action()

            elif action.__name__.startswith('deploy'):
                status = await action(amount=TokenAmount(0.0002))

            elif action.__name__.startswith('send_tx_to_arb'):
                status = await action()

            elif action.__name__.startswith('send_tx_to_base'):
                status = await action()

            else:
                status = await action(amount=TokenAmount(0.00005))

            if 'failed' not in status:
                wallet.next_initial_action_time = now + timedelta(
                    seconds=random.randint(settings.initial_actions_delay.from_, settings.initial_actions_delay.to_)
                )
                # db.commit()

                if 'deposited Aave' in status:
                    wallet.aave_depozit = True

                if 'withdraw Aave' in status:
                    wallet.aave_withdraw = True

                if 'ZORB' in status:
                    wallet.zorb_nft = True

                if 'SPG' in status:
                    wallet.spg_nft = True

                if 'DST' in status:
                    wallet.dst_nft = True

                if 'ABS' in status:
                    wallet.abs_nft = True

                if 'TY' in status:
                    wallet.ty_nft = True

                if 'SBS' in status:
                    wallet.sbs_nft = True

                if 'DBS' in status:
                    wallet.dbs_nft = True

                if 'MGB' in status:
                    wallet.mgb_nft = True

                if 'AST' in status:
                    wallet.ast_nft = True

                if 'HLC' in status:
                    wallet.hlc_nft = True

                if 'BCL' in status:
                    wallet.bcl_nft = True

                if 'BSS' in status:
                    wallet.bss_nft = True

                if 'BFR' in status:
                    wallet.bfr_nft = True

                if 'UBS' in status:
                    wallet.ubs_nft = True

                if 'LFS' in status:
                    wallet.lfs_nft = True

                if 'BTM' in status:
                    wallet.btm_nft = True

                if 'BASS' in status:
                    wallet.bas_nft = True

                if 'ARTB' in status:
                    wallet.artb_nft = True

                if 'NTM' in status:
                    wallet.ntm_nft = True

                if 'QBS' in status:
                    wallet.qbs_nft = True

                if 'BAZ' in status:
                    wallet.baz_nft = True

                if 'TIM' in status:
                    wallet.tim_nft = True

                if 'LUE' in status:
                    wallet.lue_nft = True

                if 'BLL' in status:
                    wallet.bll_nft = True

                if 'UNI' in status:
                    wallet.uni_nft = True

                if 'BSW' in status:
                    wallet.bsw_nft = True

                if 'SQU' in status:
                    wallet.squ_nft = True

                if 'BRY' in status:
                    wallet.bry_nft = True

                if 'PSS' in status:
                    wallet.pss_nft = True

                if 'DIF' in status:
                    wallet.dif_nft = True

                db.commit()

                logger.success(f'{wallet.address}: {status}')

                logger.info(f'The next closest initial action will be performed at {wallet.next_initial_action_time}')

                await asyncio.sleep(delay)

            else:
                wallet.next_initial_action_time = now + timedelta(seconds=random.randint(10 * 60, 20 * 60))
                db.commit()
                logger.error(f'{wallet.address}: {status}')

        except BaseException as e:
            logger.exception(f'Something went wrong: {e}')

        finally:
            await asyncio.sleep(delay)
