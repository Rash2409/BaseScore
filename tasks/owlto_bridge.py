import random
from web3.types import TxParams
from loguru import logger
from tasks.base import Base
from libs.eth_async.data.models import TokenAmount
from data.models import Contracts
import asyncio
import aiohttp


class Owlto(Base):

    API_URL = ' https://owlto.finance/api/bridge_api/v1/'

    async def send_tx_to_arb(self, amount: TokenAmount | None = None):

        if not amount:
            amount = await self.client.wallet.balance(token=Contracts.USDC.address)

        amount_new = TokenAmount(amount.Wei - 2500000)

        tx_data = await self.get_build_tx_arb(amount=amount_new)

        owlto_contract = await self.client.contracts.get(contract_address=Contracts.OWLTO)

        if await self.approve_interface(
                token_address=Contracts.USDC.address,
                spender=owlto_contract.address,
                amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'can not approve'

        tx_body = tx_data['data']['txs']['transfer_body']

        value = int(tx_body['value'])
        data = tx_body['data']
        to = tx_body['to']

        tx_params = TxParams(
            to=to,
            data=data,
            value=value
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)

        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)

        if receipt:
            logger.success(f'{amount.Ether} USDC was bridged to Arbitrum | Base -> Owlto | {tx.hash.hex()}')
            return f'{amount.Ether} USDC was bridged to Arbitrum | Base -> Owlto | {tx.hash.hex()}'

        return logger.error("Failed bridged | Base")

    async def get_build_tx_arb(self, amount):

        payload = {
            "from_address": f"{self.client.account.address}",
            "from_chain_name": "BaseMainnet",
            "to_address": f"{self.client.account.address}",
            "to_chain_name": "ArbitrumOneMainnet",
            "token_name": "USDC",
            "ui_value": f"{float(amount.Ether) / 10**6:.2f}"
        }

        async with aiohttp.ClientSession() as session:

            API_URL = 'https://owlto.finance/api/bridge_api/v1/'

            async with session.post(API_URL + "get_build_tx", json=payload,
                                    headers={"Content-Type": "application/json"}) as response:
                data = await response.json()
                return data

    async def send_tx_to_base(self, amount: TokenAmount | None = None):

        if not amount:
            amount = await self.client.wallet.balance(token=Contracts.ARBUSDC)

        amount_new = TokenAmount(amount.Wei - 1600000)

        tx_data = await self.get_build_tx_base(amount=amount_new)

        owlto_contract = await self.client.contracts.get(contract_address=Contracts.OWLTO2)

        if await self.approve_interface(
                token_address=Contracts.ARBUSDC.address,
                spender=owlto_contract.address,
                amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'can not approve'

        tx_body = tx_data['data']['txs']['transfer_body']

        value = int(tx_body['value'])
        data = tx_body['data']
        to = tx_body['to']

        tx_params = TxParams(
            to=to,
            data=data,
            value=value
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)

        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)

        if receipt:
            logger.success(f'{amount.Ether} USDC was bridged to Base | Arbitrum -> Owlto | {tx.hash.hex()}')
            return f'{amount.Ether} USDC was bridged to Base | Arbitrum -> Owlto | {tx.hash.hex()}'

        return logger.error("Failed bridged | Base")

    async def get_build_tx_base(self, amount):

        payload = {
            "from_address": f"{self.client.account.address}",
            "from_chain_name": "ArbitrumOneMainnet",
            "to_address": f"{self.client.account.address}",
            "to_chain_name": "BaseMainnet",
            "token_name": "USDC",
            "ui_value": f"{float(amount.Ether) / 10**6:.2f}"
        }

        async with aiohttp.ClientSession() as session:
            API_URL = 'https://owlto.finance/api/bridge_api/v1/'
            async with session.post(API_URL + "get_build_tx", json=payload,
                                    headers={"Content-Type": "application/json"}) as response:
                data = await response.json()
                return data
