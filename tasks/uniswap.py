import asyncio
import time
import random
from loguru import logger

from web3.types import TxParams
from web3 import Web3
from tasks.base import Base
from libs.eth_async.data.models import TxArgs, TokenAmount

from data.models import Contracts


class Uniswap(Base):

    async def eth_to_usdc(self, amount: TokenAmount, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.USDC.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.debug(f'start swap ETH to USDC | Uniswap')

        contract = await self.client.contracts.get(contract_address=Contracts.UNISWAP)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        args = TxArgs(
            commands='0x0b000604',
            inputs=[
                f'0x{"2".zfill(64)}{hex(amount.Wei)[2:].zfill(64)}',

                f'0x{"2".zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"".zfill(64)}'
                f'{"2b".zfill(64)}'
                f'42000000000000000000000000000000000000060001f4833589fcd6edb6e08f'
                f'4c7c32d4f71b54bda02913000000000000000000000000000000000000000000',

                f'0x{Contracts.USDC.address[2:].zfill(64)}'
                f'{Contracts.USDC2.address[2:].zfill(64)}'
                f'{"19".zfill(64)}',

                f'0x{Contracts.USDC.address[2:].zfill(64)}'
                f'{"1".zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}',
            ],
            deadline=int(time.time()) + 60 * 5,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('execute', args=args.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} ETH was send to USDC via Uniswap | {tx.hash.hex()}')
            return f'{amount.Ether} ETH was send to USDC | {tx.hash.hex()}'
        return f'failed swap'

    async def usdc_to_eth(self, amount: TokenAmount | None = None, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.USDC.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.debug(f'start swap from USDC to ETH | Uniswap')

        failed_text = f'Failed swap {from_token_name} to {to_token_name} | via Uniswap'

        contract = await self.client.contracts.get(contract_address=Contracts.UNISWAP)

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

        # args = TxArgs(
        #     commands='0x0a00060c',
        #     inputs=[
        #         f'0x{Contracts.USDC.address[2:].zfill(64)}'
        #         f'000000000000000000000000ffffffffffffffffffffffffffffffffffffffff'
        #         f'{"671fd6e2".zfill(64)}'
        #         f'{"".zfill(64)}'
        #         f'{Contracts.UNISWAP.address[2:].zfill(64)}'
        #         f'{"66f850ea".zfill(64)}'
        #         f'{"e0".zfill(64)}'
        #         f'{"41".zfill(64)}'
        #         f'ee381ce717887afd5ba8afb6c40d25b6b5e8b0402b0b543c1f0bda82e70be3a6'
        #         f'0d425e89479deeeb9baf57a5459388b34e8a3fb59b6022af2593714f5a0d5e67'
        #         f'1b00000000000000000000000000000000000000000000000000000000000000',
        #
        #         f'0x{"2".zfill(64)}'
        #         f'{hex(amount.Wei)[2:].zfill(64)}'
        #         f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
        #         f'{"a0".zfill(64)}'
        #         f'{"1".zfill(64)}'
        #         f'{"2b".zfill(64)}'
        #         f'833589fcd6edb6e08f4c7c32d4f71b54bda029130001f4420000000000000000'
        #         f'0000000000000000000006000000000000000000000000000000000000000000',
        #
        #         f'0x{Contracts.WETH.address[2:].zfill(64)}'
        #         f'{Contracts.WETH2.address[2:].zfill(64)}'
        #         f'{"19".zfill(64)}',
        #
        #         f'0x{"1".zfill(64)}'
        #         f'{hex(amount_out_min.Wei)[2:].zfill(64)}',
        #     ],
        #     deadline=int(time.time()) + 60 * 5,
        # )

        args = TxArgs(
            commands='0x00060c',
            inputs=[
                f'0x{"2".zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"1".zfill(64)}'
                f'{"2b".zfill(64)}'
                f'833589fcd6edb6e08f4c7c32d4f71b54bda029130001f4420000000000000000'
                f'0000000000000000000006000000000000000000000000000000000000000000',

                f'0x{Contracts.WETH.address[2:].zfill(64)}'
                f'{Contracts.WETH2.address[2:].zfill(64)}'
                f'{"19".zfill(64)}',

                f'0x{"1".zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}',
            ],
            deadline=int(time.time()) + 60 * 5,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('execute', args=args.tuple()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} USDC was send to ETH via Uniswap | {tx.hash.hex()}')
            return f'{amount.Ether} USDC was send to ETH | {tx.hash.hex()}'

        return f'failed swap'

    async def eth_to_dai(self, amount: TokenAmount, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.DAI.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.debug(f'start swap ETH to DAI | Uniswap')

        contract = await self.client.contracts.get(contract_address=Contracts.UNISWAP)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        args = TxArgs(
            commands='0x0b000604',
            inputs=[
                f'0x{"2".zfill(64)}{hex(amount.Wei)[2:].zfill(64)}',

                f'0x{"2".zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"".zfill(64)}'
                f'{"2b".zfill(64)}'
                f'42000000000000000000000000000000000000060001f450c5725949a6f0c72e'
                f'6c4a641f24049a917db0cb000000000000000000000000000000000000000000',

                f'0x{Contracts.DAI.address[2:].zfill(64)}'
                f'{Contracts.DAI2.address[2:].zfill(64)}'
                f'{"19".zfill(64)}',

                f'0x{Contracts.DAI.address[2:].zfill(64)}'
                f'{"1".zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}',
            ],
            deadline=int(time.time()) + 60 * 5,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('execute', args=args.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} ETH was send to DAI via Uniswap | {tx.hash.hex()}')
            return f'{amount.Ether} ETH was send to DAI | {tx.hash.hex()}'
        return f'failed swap'

    async def dai_to_eth(self, amount: TokenAmount | None = None, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.DAI.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.debug(f'start swap from DAI to ETH | Uniswap')

        failed_text = f'Failed swap {from_token_name} to {to_token_name} | via Uniswap'

        contract = await self.client.contracts.get(contract_address=Contracts.UNISWAP)

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

        from_token_price_dollar = await self.get_token_price(token_symbol="DAI")
        to_token_price_dollar = await self.get_token_price(token_symbol=to_token_name)
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        args = TxArgs(
            commands='0x00060c',
            inputs=[
                f'0x{"2".zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"1".zfill(64)}'
                f'{"2b".zfill(64)}'
                f'50c5725949a6f0c72e6c4a641f24049a917db0cb0001f4420000000000000000'
                f'0000000000000000000006000000000000000000000000000000000000000000',

                f'0x{Contracts.WETH.address[2:].zfill(64)}'
                f'{Contracts.WETH2.address[2:].zfill(64)}'
                f'{"19".zfill(64)}',

                f'0x{"1".zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}',
            ],
            deadline=int(time.time()) + 60 * 5,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('execute', args=args.tuple()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} DAI was send to ETH via Uniswap | {tx.hash.hex()}')
            return f'{amount.Ether} DAI was send to ETH | {tx.hash.hex()}'

        return f'failed swap'

    async def eth_to_usdbc(self, amount: TokenAmount, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.USDbC.address)

        logger.debug(f'start swap ETH to USDbC | Uniswap')

        contract = await self.client.contracts.get(contract_address=Contracts.UNISWAP)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol='USDC')
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        args = TxArgs(
            commands='0x0b000604',
            inputs=[
                f'0x{"2".zfill(64)}{hex(amount.Wei)[2:].zfill(64)}',

                f'0x{"2".zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"".zfill(64)}'
                f'{"2b".zfill(64)}'
                f'42000000000000000000000000000000000000060001f4d9aaec86b65d86f6a7'
                f'b5b1b0c42ffa531710b6ca000000000000000000000000000000000000000000',

                f'0x{Contracts.USDbC.address[2:].zfill(64)}'
                f'{Contracts.USDbC2.address[2:].zfill(64)}'
                f'{"19".zfill(64)}',

                f'0x{Contracts.USDbC.address[2:].zfill(64)}'
                f'{"1".zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}',
            ],
            deadline=int(time.time()) + 60 * 5,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('execute', args=args.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} ETH was send to USDbC via Uniswap | {tx.hash.hex()}')
            return f'{amount.Ether} ETH was send to USDbC | {tx.hash.hex()}'

        return f'failed swap'

    async def usdbc_to_eth(self, amount: TokenAmount | None = None, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.USDbC.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.debug(f'start swap from USDbC to ETH | Uniswap')

        failed_text = f'Failed swap {from_token_name} to {to_token_name} | via Uniswap'

        contract = await self.client.contracts.get(contract_address=Contracts.UNISWAP)

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

        args = TxArgs(
            commands='0x00060c',
            inputs=[
                f'0x{"2".zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"1".zfill(64)}'
                f'{"2b".zfill(64)}'
                f'd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA0001f4420000000000000000'
                f'0000000000000000000006000000000000000000000000000000000000000000',

                f'0x{Contracts.WETH.address[2:].zfill(64)}'
                f'{Contracts.WETH2.address[2:].zfill(64)}'
                f'{"19".zfill(64)}',

                f'0x{"1".zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}',
            ],
            deadline=int(time.time()) + 60 * 5,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('execute', args=args.tuple()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} USDbC was send to ETH via Uniswap | {tx.hash.hex()}')
            return f'{amount.Ether} USbDC was send to ETH | {tx.hash.hex()}'

        return f'failed swap'

    async def eth_to_axlusdc(self, amount: TokenAmount, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.axlUSDC.address)

        logger.debug(f'start swap ETH to axlUSDC | Uniswap')

        contract = await self.client.contracts.get(contract_address=Contracts.UNISWAP)

        from_token_price_dollar = await self.get_token_price(token_symbol=from_token_name)
        to_token_price_dollar = await self.get_token_price(token_symbol='USDC')
        amount_out_min = TokenAmount(
            amount=float(amount.Ether) * from_token_price_dollar / to_token_price_dollar * (100 - slippage) / 100,
            decimals=await self.client.transactions.get_decimals(contract=to_token_address)
        )

        args = TxArgs(
            commands='0x0b000604',
            inputs=[
                f'0x{"2".zfill(64)}{hex(amount.Wei)[2:].zfill(64)}',

                f'0x{"2".zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"".zfill(64)}'
                f'{"42".zfill(64)}'
                f'42000000000000000000000000000000000000060001f4d9aaec86b65d86f6a7'
                f'b5b1b0c42ffa531710b6ca000064eb466342c4d449bc9f53a865d5cb90586f40'
                f'5215000000000000000000000000000000000000000000000000000000000000',

                f'0x{Contracts.axlUSDC.address[2:].zfill(64)}'
                f'{Contracts.axlUSDC2.address[2:].zfill(64)}'
                f'{"19".zfill(64)}',

                f'0x{Contracts.axlUSDC.address[2:].zfill(64)}'
                f'{"1".zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}',
            ],
            deadline=int(time.time()) + 60 * 5,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('execute', args=args.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} Ether was send to axlUSDC via Uniswap | {tx.hash.hex()}')
            return f'{amount.Ether} Ether was send to axlUSDC | {tx.hash.hex()}'

        return f'failed swap'

    async def axlusdc_to_eth(self, amount: TokenAmount | None = None, slippage: float = 1.0) -> str:

        from_token_address = Web3.to_checksum_address(Contracts.axlUSDC.address)
        from_token = await self.client.contracts.default_token(contract_address=from_token_address)
        from_token_name = await from_token.functions.symbol().call()

        to_token_address = Web3.to_checksum_address(Contracts.WETH.address)
        to_token = await self.client.contracts.default_token(contract_address=to_token_address)
        to_token_name = await to_token.functions.symbol().call()

        logger.debug(f'start swap from axlUSDC to ETH | Uniswap')

        failed_text = f'Failed swap {from_token_name} to {to_token_name} | via Uniswap'

        contract = await self.client.contracts.get(contract_address=Contracts.UNISWAP)

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

        args = TxArgs(
            commands='0x00060c',
            inputs=[
                f'0x{"2".zfill(64)}'
                f'{hex(amount.Wei)[2:].zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}'
                f'{"a0".zfill(64)}'
                f'{"1".zfill(64)}'
                f'{"42".zfill(64)}'
                f'eb466342c4d449bc9f53a865d5cb90586f405215000064d9aaec86b65d86f6a7'
                f'b5b1b0c42ffa531710b6ca0001f4420000000000000000000000000000000000'
                f'0006000000000000000000000000000000000000000000000000000000000000',

                f'0x{Contracts.WETH.address[2:].zfill(64)}'
                f'{Contracts.WETH2.address[2:].zfill(64)}'
                f'{"19".zfill(64)}',

                f'0x{"1".zfill(64)}'
                f'{hex(amount_out_min.Wei)[2:].zfill(64)}',
            ],
            deadline=int(time.time()) + 60 * 5,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('execute', args=args.tuple()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(self.client, timeout=300)
        if receipt:
            logger.success(f'{amount.Ether} USDbC was send to ETH via Uniswap | {tx.hash.hex()}')
            return f'{amount.Ether} USDbC was send to ETH | {tx.hash.hex()}'

        return f'failed swap'
