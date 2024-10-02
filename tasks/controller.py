from libs.eth_async.client import Client
# from libs.eth_async.data.models import Networks
# from zksync_explorer.explorer_api import APIFunctions
# from data.models import Contracts, Settings
from tasks.base import Base
from tasks.mint_nft import MintNft
from tasks.aave import Aave
from tasks.aerodrom import Aerodrom
from tasks.owlto_bridge import Owlto
from tasks.owlto_deploy import Deploy
from tasks.swapbased import Swapbased
from tasks.uniswap import Uniswap


class Controller(Base):
    def __init__(self, client: Client):
        super().__init__(client)

        self.base = Base(client=client)
        self.mint_nft = MintNft(client=client)
        self.aave = Aave(client=client)
        self.aerodrom = Aerodrom(client=client)
        self.owlto = Owlto(client=client)
        self.deploy = Deploy(client=client)
        self.swapbased = Swapbased(client=client)
        self.uniswap = Uniswap(client=client)

    # async def made_ethereum_bridge(self) -> bool:
    #     client = Client(private_key='', network=Networks.Ethereum)
    #     return bool(await client.transactions.find_txs(
    #         contract=Contracts.ETH_OFFICIAL_BRIDGE,
    #         function_name='requestL2Transaction',
    #         address=self.client.account.address,
    #     ))

    # async def count_swaps(self, tx_list: list[dict] | None = None):
    #     settings = Settings()
    #     result_count = 0
    #
    #     api_oklink = APIFunctions(url='https://www.oklink.com', key=settings.oklink_api_key)
    #
    #     if not tx_list:
    #         tx_list = await api_oklink.account.txlist_all(
    #             address=self.client.account.address
    #         )
    #
    #     # Maveric
    #     result_count += len(await api_oklink.account.find_tx_by_method_id(
    #         address=self.client.account.address,
    #         to=Contracts.MAVERICK.address,
    #         method_id='0xac9650d8',
    #         tx_list=tx_list
    #     ))
    #
    #     # Mute eth -> token
    #     result_count += len(await api_oklink.account.find_tx_by_method_id(
    #         address=self.client.account.address,
    #         to=Contracts.MUTE.address,
    #         method_id='0x51cbf10f',
    #         tx_list=tx_list
    #     ))
    #
    #     # Mute token -> eth
    #     result_count += len(await api_oklink.account.find_tx_by_method_id(
    #         address=self.client.account.address,
    #         to=Contracts.MUTE.address,
    #         method_id='0x3f464b16',
    #         tx_list=tx_list
    #     ))
    #
    #     # SpaceFi eth -> token
    #     result_count += len(await api_oklink.account.find_tx_by_method_id(
    #         address=self.client.account.address,
    #         to=Contracts.SPACE_FI.address,
    #         method_id='0x7ff36ab5',
    #         tx_list=tx_list
    #     ))
    #
    #     # SpaceFi token -> eth
    #     result_count += len(await api_oklink.account.find_tx_by_method_id(
    #         address=self.client.account.address,
    #         to=Contracts.SPACE_FI.address,
    #         method_id='0x18cbafe5',
    #         tx_list=tx_list
    #     ))
    #
    #     # SyncSwap
    #     result_count += len(await api_oklink.account.find_tx_by_method_id(
    #         address=self.client.account.address,
    #         to=Contracts.SYNC_SWAP.address,
    #         method_id='0x2cc4081e',
    #         tx_list=tx_list
    #     ))
    #
    #     return result_count

    # async def count_liquidity(self, txs: list[dict] | None = None):
    #     ...
