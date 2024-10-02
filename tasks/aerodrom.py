import time
import asyncio
import random
from web3.types import TxParams
from web3 import Web3
from loguru import logger

from tasks.base import Base
from libs.eth_async.data.models import TxArgs, TokenAmount
from data.models import Contracts


class Aerodrom(Base):

    async def eth_to_usdc(self, amount: TokenAmount, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.USDC.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.info(f'Start swap ETH to USDC | Aerodrom')

        aerodrom_contract = await self.client.contracts.get(contract_address=Contracts.AERODROM2)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        args = TxArgs(
            commands='0x0b0800',
            inputs=[
                f'0x{Contracts.AERODROM2.address[2:].zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}',

                f'0x{Contracts.AERODROM2.address[2:].zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{"".zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"".zfill(64)}'
                f'{"1".zfill(64)}'
                f'{Contracts.WETH.address[2:].zfill(64)}'
                f'{Contracts.USDbC.address[2:].zfill(64)}'
                f'{"1".zfill(64)}',

                f'0x{self.client.account.address[2:].zfill(64)}'
                f'8000000000000000000000000000000000000000000000000000000000000000'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"".zfill(64)}'
                f'{"2b".zfill(64)}'
                f'd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca000001833589fcd6edb6e08f'
                f'4c7c32d4f71b54bda02913000000000000000000000000000000000000000000',
            ],
        )

        tx_params = TxParams(
            to=aerodrom_contract.address,
            data=aerodrom_contract.encodeABI('execute', args=args.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} ETH was swapped to {to_token_name} | via Aerodrom: {tx.hash.hex()}')
            return f'{amount.Ether} ETH was swapped to {to_token_name} | via Aerodrom: {tx.hash.hex()}'
        return f'Failed swap {from_token_name} to {to_token_name} via Swap based'

    async def usdc_to_eth(self, amount: TokenAmount | None = None, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.USDC.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.info(f'Start swap from USDC to ETH | Aerodrom')

        failed_text = f'Failed swap {from_token_name} to {to_token_name} | via Aerodrom'

        aerodrom_contract = await self.client.contracts.get(contract_address=Contracts.AERODROM2)

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        if await self.approve_interface(
                token_address=from_token.address,
                spender=aerodrom_contract.address,
                amount=amount
        ):
            await asyncio.sleep(random.randint(5, 10))
        else:
            return f'{failed_text} | can not approve'

        from_token_price_dollar = await self.get_token_price(token_symbol="USDC")
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        args = TxArgs(
            commands='0x00080c',
            inputs=[
                f'0x0000000000000000000000002578365b3dfa7ffe60108e181efb79feddec2319'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{"".zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"1".zfill(64)}'
                f'{"2b".zfill(64)}'
                f'833589fcd6edb6e08f4c7c32d4f71b54bda02913000064cbb7c0000ab88b473b'
                f'1f5afd9ef808440eed33bf000000000000000000000000000000000000000000',

                f'0x{Contracts.AERODROM2.address[2:].zfill(64)}'
                f'{"".zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"".zfill(64)}'
                f'{"1".zfill(64)}'
                f'000000000000000000000000cbb7c0000ab88b473b1f5afd9ef808440eed33bf'
                f'0000000000000000000000004200000000000000000000000000000000000006'
                f'0000000000000000000000000000000000000000000000000000000000000000',

                f'0x{self.client.account.address[2:].zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}',
            ],
        )

        tx_params = TxParams(
            to=aerodrom_contract.address,
            data=aerodrom_contract.encodeABI('execute', args=args.tuple()),
            value=0
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} {from_token_name} was swapped to ETH via Aerodrom: {tx.hash.hex()}')
            return f'{amount.Ether} {from_token_name} was swapped to ETH via Aerodromd: {tx.hash.hex()}'
        return f'Failed swap {from_token_name} to {to_token_name} via Aerodrom'
