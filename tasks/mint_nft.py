from web3.types import TxParams

from tasks.base import Base
from libs.eth_async.data.models import TxArgs, TokenAmount, RawContract
from data.models import Contracts
from loguru import logger


class MintNft(Base):

    async def _mint_nft(
            self,
            amount: TokenAmount,
            contract_nft: RawContract,
    ) -> str:

        contract = await self.client.contracts.get(contract_address=contract_nft)

        address = self.client.account.address

        logger.info(f'{contract_nft.title} start minting')

        args = TxArgs(

        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('mint', args=args.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{contract_nft.title}| WAS MINTED VIA BASE | ADDRESS - {address}'
        return f'mint was failed'

    async def mint_zorb(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.ZORB_NFT
        )

    async def mint_spg(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.SPG_NFT
        )

    async def mint_dst(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.DST_NFT
        )

    async def mint_abs(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.ABS_NFT
        )

    async def mint_ty(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.TY_NFT
        )

    async def mint_sbs(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.SBS_NFT
        )

    async def mint_dbs(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.DBS_NFT
        )

    async def mint_mgb(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.MGB_NFT
        )

    async def mint_ast(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.AST_NFT
        )

    async def mint_hlc(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.HLC_NFT
        )

    async def mint_bcl(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.BCL_NFT
        )

    async def mint_bss(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.BSS_NFT
        )

    async def mint_bfr(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.BFR_NFT
        )

    async def mint_ubs(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.UBS_NFT
        )

    async def mint_lfs(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.LFS_NFT
        )

    async def mint_btm(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.BTM_NFT
        )

    async def mint_bas(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.BAS_NFT
        )

    async def mint_artb(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.ARTB_NFT
        )

    async def mint_ntm(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.NTM_NFT
        )

    async def mint_qbs(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.QBS_NFT
        )

    async def mint_baz(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.BAZ_NFT
        )

    async def mint_tim(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.TIM_NFT
        )

    async def mint_lue(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.LUE_NFT
        )

    async def mint_bll(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.BLL_NFT
        )

    async def mint_uni(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.UNI_NFT
        )

    async def mint_bsw(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.BSW_NFT
        )

    async def mint_squ(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.SQU_NFT
        )

    async def mint_bry(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.BRY_NFT
        )

    async def mint_pss(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.PSS_NFT
        )

    async def mint_dif(self, amount: TokenAmount) -> str:
        return await self._mint_nft(
            amount=amount,
            contract_nft=Contracts.DIF_NFT
        )

    async def mint_summer_game(
            self,
            amount: TokenAmount,
            contract_nft: RawContract,
    ) -> str:

        contract = await self.client.contracts.get(contract_address=contract_nft)

        address = self.client.account.address

        logger.info(f'{contract_nft.title} start minting')

        args = TxArgs(

        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('mint', args=args.tuple()),
            value=amount.Wei
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)
        if receipt:
            return f'{contract_nft.title}| WAS MINTED VIA BASE | ADDRESS - {address}'
        return f'mint was failed'