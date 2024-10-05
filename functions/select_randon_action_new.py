import asyncio
import random

from loguru import logger

from tasks.controller import Controller
from libs.eth_async.data.models import TokenAmount
from data.models import Settings, Contracts
from utils.db_api.models import Wallet


async def select_random_action(controller: Controller, controller2: Controller, wallet: Wallet):
    settings = Settings()

    possible_actions = []
    weights = []

    eth_balance = await controller.client.wallet.balance()

    if float(eth_balance.Ether) < settings.minimal_balance:
        return 'Insufficient balance'

    usdc_balance = await controller.client.wallet.balance(token=Contracts.USDC)
    axlusdc_balance = await controller.client.wallet.balance(token=Contracts.axlUSDC)
    usdbc_balance = await controller.client.wallet.balance(token=Contracts.USDbC)
    arbeth_balance = await controller2.client.wallet.balance()
    arbusdc_balance = await controller2.client.wallet.balance(token=Contracts.ARBUSDC)

    has_stablecoins = any([usdc_balance.Wei, axlusdc_balance.Wei, usdbc_balance.Wei, arbusdc_balance.Wei])

    if has_stablecoins:
        logger.info(f"{wallet.address} | Найдены стейблкоины. Выбор действия с ними...")

        if usdc_balance.Wei:
            possible_actions += [
                controller.aerodrom.usdc_to_eth,
            ]
            weights += [1, ]

        if usdc_balance.Wei and arbeth_balance.Wei:
            possible_actions += [
                controller.owlto.send_tx_to_arb,
            ]
            weights += [1, ]

        if axlusdc_balance.Wei:
            possible_actions += [
                controller.swapbased.axlusdc_to_eth,
            ]
            weights += [1,]

        if usdbc_balance.Wei:
            possible_actions += [
                controller.swapbased.usdbc_to_eth,
            ]
            weights += [1,]

        if arbusdc_balance.Wei > TokenAmount(1.7, decimals=6).Wei and arbeth_balance.Wei:
            possible_actions += [
                controller2.owlto.send_tx_to_base
            ]
            weights += [100]

    #  Логика для ETH теперь выполняется, даже если есть стейблкоины, но недостаточно для owlto.send_tx_to_base
    if not has_stablecoins or not possible_actions:  # Если нет стейблкоинов или не выбрано ни одного действия с ними
        logger.info(f"{wallet.address} | Стейблкоины не найдены или недостаточно для обмена. Выбор действия с ETH...")

        if eth_balance:
            possible_actions += [
                controller.aerodrom.eth_to_usdc,
                controller.swapbased.eth_to_usdc,
                controller.swapbased.eth_to_usdbc,
                controller.swapbased.eth_to_axlusdc,
                controller.uniswap.eth_to_usdc,
                controller.uniswap.eth_to_usdbc,
                controller.uniswap.eth_to_axlusdc,
                controller.deploy.deploy
            ]
            weights += [0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.5]

            if wallet.aave_depozit == False:
                possible_actions.append(controller.aave.depozit_eth)
                weights += [0.5, ]
            if wallet.aave_depozit == True and wallet.aave_withdraw == False:
                possible_actions.append(controller.aave.withdraw_eth)
                weights += [0.5, ]

            if wallet.zorb_nft == False:
                possible_actions += [controller.mint_nft.mint_zorb, ]
                weights += [0.012, ]
            

            if wallet.spg_nft == False:
                possible_actions += [controller.mint_nft.mint_spg, ]
                weights += [0.012, ]
            

            if wallet.dst_nft == False:
                possible_actions += [controller.mint_nft.mint_dst, ]
                weights += [0.012, ]
            

            if wallet.abs_nft == False:
                possible_actions += [controller.mint_nft.mint_abs, ]
                weights += [0.012, ]
            

            if wallet.ty_nft == False:
                possible_actions += [controller.mint_nft.mint_ty, ]
                weights += [0.012, ]
            

            if wallet.sbs_nft == False:
                possible_actions += [controller.mint_nft.mint_sbs, ]
                weights += [0.012, ]
            

            if wallet.dbs_nft == False:
                possible_actions += [controller.mint_nft.mint_dbs, ]
                weights += [0.012, ]
            

            if wallet.mgb_nft == False:
                possible_actions += [controller.mint_nft.mint_mgb, ]
                weights += [0.012, ]
            

            if wallet.ast_nft == False:
                possible_actions += [controller.mint_nft.mint_ast, ]
                weights += [0.012, ]
            

            if wallet.hlc_nft == False:
                possible_actions += [controller.mint_nft.mint_hlc, ]
                weights += [0.012, ]
            

            if wallet.bcl_nft == False:
                possible_actions += [controller.mint_nft.mint_bcl, ]
                weights += [0.012, ]
            

            if wallet.bss_nft == False:
                possible_actions += [controller.mint_nft.mint_bss, ]
                weights += [0.012, ]
            

            if wallet.bfr_nft == False:
                possible_actions += [controller.mint_nft.mint_bfr, ]
                weights += [0.012, ]
            

            if wallet.ubs_nft == False:
                possible_actions += [controller.mint_nft.mint_ubs, ]
                weights += [0.012, ]
            

            if wallet.lfs_nft == False:
                possible_actions += [controller.mint_nft.mint_lfs, ]
                weights += [0.012, ]
            

            if wallet.btm_nft == False:
                possible_actions += [controller.mint_nft.mint_btm, ]
                weights += [0.012, ]
            

            if wallet.bas_nft == False:
                possible_actions += [controller.mint_nft.mint_bas, ]
                weights += [0.012, ]
            

            if wallet.artb_nft == False:
                possible_actions += [controller.mint_nft.mint_artb, ]
                weights += [0.012, ]
            

            if wallet.ntm_nft == False:
                possible_actions += [controller.mint_nft.mint_ntm, ]
                weights += [0.012, ]
            

            if wallet.qbs_nft == False:
                possible_actions += [controller.mint_nft.mint_qbs, ]
                weights += [0.012, ]
            

            if wallet.baz_nft == False:
                possible_actions += [controller.mint_nft.mint_baz, ]
                weights += [0.012, ]
            

            if wallet.tim_nft == False:
                possible_actions += [controller.mint_nft.mint_tim, ]
                weights += [0.012, ]
            

            if wallet.lue_nft == False:
                possible_actions += [controller.mint_nft.mint_lue, ]
                weights += [0.012, ]
            

            if wallet.bll_nft == False:
                possible_actions += [controller.mint_nft.mint_bll, ]
                weights += [0.012, ]
            

            if wallet.uni_nft == False:
                possible_actions += [controller.mint_nft.mint_uni, ]
                weights += [0.012, ]
            

            if wallet.bsw_nft == False:
                possible_actions += [controller.mint_nft.mint_bsw, ]
                weights += [0.012, ]
            

            if wallet.squ_nft == False:
                possible_actions += [controller.mint_nft.mint_squ, ]
                weights += [0.012, ]
            

            if wallet.bry_nft == False:
                possible_actions += [controller.mint_nft.mint_bry, ]
                weights += [0.012, ]
            

            if wallet.pss_nft == False:
                possible_actions += [controller.mint_nft.mint_pss, ]
                weights += [0.012, ]
            

            if wallet.dif_nft == False:
                possible_actions += [controller.mint_nft.mint_dif, ]
                weights += [0.012, ]

        else:
            logger.warning('Insufficient balance')
                
    if possible_actions:
        await asyncio.sleep(15)
        action = random.choices(possible_actions, weights=weights)[0]
        return action

    logger.warning(f"{wallet.address} | Действие не выбрано. Возможно, нет доступных опций. | Processed")
    return None
