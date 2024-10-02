import time
import asyncio
import random
from web3.types import TxParams
from web3 import Web3
from loguru import logger
from tasks.base import Base
from libs.eth_async.data.models import TxArgs, TokenAmount
from data.models import Contracts


class Swapbased(Base):

    async def eth_to_axlusdc(self, amount: TokenAmount, slippage: float = 3.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.axlUSDC.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.info(f'start swap ETH to axlUSDC | Swapbased')

        contract = await self.client.contracts.get(contract_address=Contracts.SWAP_BASED)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol='USDC')
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        params = TxArgs(
            amountOutMin=amount_out_min.Wei,
            path=[from_token_address, to_token_address],
            to=self.client.account.address,
            deadline=int(time.time() + 20 * 60)
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swapExactETHForTokens', args=params.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} ETH was swapped to {to_token_name} via Swapbased: {tx.hash.hex()}')
            return f'{amount.Ether} ETH was swapped to {to_token_name} via Swapbased: {tx.hash.hex()}'

        return f'Failed swap {from_token_name} to {to_token_name} via Swapbased'

    async def axlusdc_to_eth(self, amount: TokenAmount | None = None, slippage: float = 3.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.axlUSDC.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.info(f'start swap from axlUSDC to ETH | Swapbased')

        failed_text = f'Failed swap {from_token_name} to {to_token_name} via Swapbased'

        contract = await self.client.contracts.get(contract_address=Contracts.SWAP_BASED)

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        if await self.approve_interface(
                token_address=from_token.address,
                spender=contract.address,
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

        params = TxArgs(
            amountIn=amount.Wei,
            amountOutMin=amount_out_min.Wei,
            path=[from_token_address, to_token_address],
            to=self.client.account.address,
            deadline=int(time.time() + 20 * 60)
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swapExactTokensForETH', args=params.tuple()),
            value=0
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} axlUSDC was swapped to ETH via Swapbased: {tx.hash.hex()}')
            return f'{amount.Ether} axlUSDC was swapped to ETH via Swapbased: {tx.hash.hex()}'
        return f'Failed swap {from_token_name} to {to_token_name} via Swap based'

    async def eth_to_dai(self, amount: TokenAmount, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.DAI.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.info(f'start swap ETH to DAI | Swapbased')

        contract = await self.client.contracts.get(contract_address=Contracts.SWAP_BASED)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol='USDC')
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        params = TxArgs(
            amountOutMin=amount_out_min.Wei,
            path=[from_token_address, Contracts.USDbC.address, to_token_address],
            to=self.client.account.address,
            deadline=int(time.time() + 20 * 60)
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swapExactETHForTokens', args=params.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} ETH was swapped to {to_token_name} via Swapbased: {tx.hash.hex()}')
            return f'{amount.Ether} ETH was swapped to {to_token_name} via Swapbased: {tx.hash.hex()}'

        return f'Failed swap {from_token_name} to {to_token_name} via Swap based'

    async def eth_to_usdbc(self, amount: TokenAmount, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.USDbC.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.info(f'start swap ETH to USDbC | Swapbased')

        contract = await self.client.contracts.get(contract_address=Contracts.SWAP_BASED)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol='USDC')
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        params = TxArgs(
            amountOutMin=amount_out_min.Wei,
            path=[from_token_address, to_token_address],
            to=self.client.account.address,
            deadline=int(time.time() + 20 * 60)
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swapExactETHForTokens', args=params.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} ETH was swapped to {to_token_name} via Swapbased: {tx.hash.hex()}')
            return f'{amount.Ether} ETH was swapped to {to_token_name} via Swapbased: {tx.hash.hex()}'

        return f'Failed swap {from_token_name} to {to_token_name} via Swap based'

    async def usdbc_to_eth(self, amount: TokenAmount | None = None, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.USDbC.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.info(f'start swap from USDbC to ETH | Swapbased')

        failed_text = f'Failed swap {from_token_name} to {to_token_name} via Swap based'

        contract = await self.client.contracts.get(contract_address=Contracts.SWAP_BASED)

        if not amount:
            amount = await self.client.wallet.balance(token=from_token)

        if await self.approve_interface(
                token_address=from_token.address,
                spender=contract.address,
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

        params = TxArgs(
            amountIn=amount.Wei,
            amountOutMin=amount_out_min.Wei,
            path=[from_token_address, to_token_address],
            to=self.client.account.address,
            deadline=int(time.time() + 20 * 60)
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swapExactTokensForETH', args=params.tuple()),
            value=0
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} USDbC was swapped to ETH via Swapbased: {tx.hash.hex()}')
            return f'{amount.Ether} USDbC was swapped to ETH via Swapbased: {tx.hash.hex()}'
        return f'Failed swap {from_token_name} to {to_token_name} via Swap based'

    async def eth_to_usdc(self, amount: TokenAmount, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.USDC.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.info(f'start swap ETH to USDC | Swapbased')

        contract = await self.client.contracts.get(contract_address=Contracts.SWAP_BASED)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol='USDC')
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        params = TxArgs(
            amountOutMin=amount_out_min.Wei,
            path=[from_token_address, to_token_address],
            to=self.client.account.address,
            deadline=int(time.time() + 20 * 60)
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('swapExactETHForTokens', args=params.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} ETH was swapped to {to_token_name} via Swapbased: {tx.hash.hex()}')
            return f'{amount.Ether} ETH was swapped to {to_token_name} via Swapbased: {tx.hash.hex()}'
        return f'Failed swap {from_token_name} to {to_token_name} via Swap based'
