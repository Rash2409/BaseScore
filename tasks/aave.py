import asyncio
import random
from web3.types import TxParams
from loguru import logger

from tasks.base import Base
from libs.eth_async.data.models import TxArgs, TokenAmount
from data.models import Contracts


class Aave(Base):

    async def depozit_eth(self, amount: TokenAmount) -> str:

        logger.info(f'Start deposit ETH | Aave')

        contract = await self.client.contracts.get(contract_address=Contracts.AAVE)

        params = TxArgs(
            undefined='0xA238Dd80C259a72e81d7e4664a9801593F98d1c5',
            onBehalfOf=self.client.account.address,
            referralCode=0
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('depositETH', args=params.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} ETH was deposited Aave: {tx.hash.hex()}')
            return 'deposited Aave'
        return f'Failed depozit'

    async def withdraw_eth(self, amount: TokenAmount | None = None) -> str:

        logger.info(f'Start withdraw ETH | Aave')

        contract = await self.client.contracts.get(contract_address=Contracts.AAVE)

        from_token = await self.client.contracts.default_token(contract_address=Contracts.aBasWETH.address)

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        if await self.approve_interface(
                token_address=Contracts.aBasWETH.address,
                spender=contract.address,
                amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'Can not approve'

        params = TxArgs(
            undefined='0xA238Dd80C259a72e81d7e4664a9801593F98d1c5',
            amount=amount.Wei,
            to=self.client.account.address
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('withdrawETH', args=params.tuple()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} ETH was withdrawed Aave: {tx.hash.hex()}')
            return 'withdraw Aave'
        return f'Failed withdraw'
