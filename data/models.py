import json
from dataclasses import dataclass

from libs.py_okx_async.models import OKXCredentials
from libs.eth_async.utils.files import read_json
from libs.eth_async.classes import AutoRepr, Singleton
from libs.eth_async.data.models import RawContract, DefaultABIs

from data.config import SETTINGS_FILE, ABIS_DIR


@dataclass
class WalletCSV:
    header = ['private_key', 'proxy']

    def __init__(self, private_key: str, proxy: str):
        self.private_key = private_key
        self.proxy = proxy


@dataclass
class FromTo:
    from_: int | float
    to_: int | float


class OkxModel:
    required_minimum_balance: float
    withdraw_amount: FromTo
    delay_between_withdrawals: FromTo
    credentials: OKXCredentials


class Settings(Singleton, AutoRepr):
    def __init__(self):
        json_data = read_json(path=SETTINGS_FILE)

        self.okx = OkxModel()
        self.okx.withdraw_amount = FromTo(
            from_=json_data['okx']['withdraw_amount']['from'],
            to_=json_data['okx']['withdraw_amount']['to'],
        )

        self.okx.delay_between_withdrawals = FromTo(
            from_=json_data['okx']['delay_between_withdrawals']['from'],
            to_=json_data['okx']['delay_between_withdrawals']['to'],
        )
        self.okx.credentials = OKXCredentials(
            api_key=json_data['okx']['credentials']['api_key'],
            secret_key=json_data['okx']['credentials']['secret_key'],
            passphrase=json_data['okx']['credentials']['passphrase']
        )

        self.maximum_gas_price: int = json_data['maximum_gas_price']

        self.initial_actions_delay: FromTo = FromTo(
            from_=json_data['initial_actions_delay']['from'], to_=json_data['initial_actions_delay']['to']
        )

        self.eth_amount_for_swap: FromTo = FromTo(
            from_=json_data['eth_amount_for_swap']['from'], to_=json_data['eth_amount_for_swap']['to']
        )
        self.eth_amount_for_aave: FromTo = FromTo(
            from_=json_data['eth_amount_for_aave']['from'], to_=json_data['eth_amount_for_aave']['to']
        )


class Contracts(Singleton):

    WETH = RawContract(
        title='WETH',
        address='0x4200000000000000000000000000000000000006',
        abi=DefaultABIs.Token
    )

    WETH2 = RawContract(
        title='WETH2',
        address='0x5d64D14D2CF4fe5fe4e65B1c7E3D11e18D493091',
        abi=DefaultABIs.Token
    )

    USDC = RawContract(
        title='USDC',
        address='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
        abi=DefaultABIs.Token
    )

    ARBUSDC = RawContract(
        title='ARBUSDC',
        address='0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
        abi=DefaultABIs.Token
    )

    USDC2 = RawContract(
        title='USDC2',
        address='0x7FFC3DBF3B2b50Ff3A1D5523bc24Bb5043837B14',
        abi=DefaultABIs.Token
    )

    axlUSDC = RawContract(
        title='axlUSDC',
        address='0xEB466342C4d449BC9f53A865D5Cb90586f405215',
        abi=DefaultABIs.Token
    )

    axlUSDC2 = RawContract(
        title='axlUSDC2',
        address='0x5d64D14D2CF4fe5fe4e65B1c7E3D11e18D493091',
        abi=DefaultABIs.Token
    )

    aBasWETH = RawContract(
        title='aBasWETH',
        address='0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7',
        abi=DefaultABIs.Token
    )

    DAI = RawContract(
        title='DAI',
        address='0x50c5725949a6f0c72e6c4a641f24049a917db0cb',
        abi=DefaultABIs.Token
    )

    DAI2 = RawContract(
        title='DAI2',
        address='0x5d64D14D2CF4fe5fe4e65B1c7E3D11e18D493091',
        abi=DefaultABIs.Token
    )

    USDbC = RawContract(
        title='USDbC',
        address='0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA',
        abi=DefaultABIs.Token
    )

    USDbC2 = RawContract(
        title='USDbC2',
        address='0x5d64D14D2CF4fe5fe4e65B1c7E3D11e18D493091',
        abi=DefaultABIs.Token
    )

    AERO = RawContract(
        title='AERO',
        address='0x940181a94A35A4569E4529A3CDfB74e38FD98631',
        abi=DefaultABIs.Token
    )

    AAVE = RawContract(
        title='aave',
        address='0x8be473dCfA93132658821E67CbEB684ec8Ea2E74',
        abi=read_json(path=(ABIS_DIR, 'aave.json'))
    )

    AERODROM = RawContract(
        title='aerodrom',
        address='0xcf77a3ba9a5ca399b7c97c74d54e5b1beb874e43',
        abi=read_json(path=(ABIS_DIR, 'aerodrom.json'))
    )

    AERODROM2 = RawContract(
        title='aerodrom2',
        address='0x6Cb442acF35158D5eDa88fe602221b67B400Be3E',
        abi=read_json(path=(ABIS_DIR, 'aerodrom2.json'))
    )

    UNISWAP = RawContract(
        title='uniswap',
        address='0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD',
        abi=read_json(path=(ABIS_DIR, 'uniswap.json'))
    )

    OWLTO = RawContract(
        title='owlto',
        address='0xC626845BF4E6a5802Ef774dA0B3DfC6707F015F7',
        abi=read_json(path=(ABIS_DIR, 'owlto.json'))
    )

    OWLTO2 = RawContract(
        title='owlto2',
        address='0x0e83DEd9f80e1C92549615D96842F5cB64A08762',
        abi=read_json(path=(ABIS_DIR, 'owlto.json'))
    )

    AERO_POOL = RawContract(
        title='AERO_PL',
        address='0x420DD381b31aEf6683db6B902084cB0FFECe40Da',
        abi=DefaultABIs.Token
    )

    SWAP_BASED = RawContract(
        title='swap_based',
        address='0xaaa3b1f1bd7bcc97fd1917c18ade665c5d31f066',
        abi=read_json(path=(ABIS_DIR, 'swapbased.json'))
    )

    # NFT
    ZORB_NFT = RawContract(
        title='ZORB',
        address='0x8399cbfb3db9e568eb158eb77be11eeaaa3e144a',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    SPG_NFT = RawContract(
        title='SPG',
        address='0xea10934dce66a071cbde9a10da7a8b7686d2cd30',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    DST_NFT = RawContract(
        title='DST',
        address='0xe850f88e37aefa00823b9bc2ae692362896f5c53',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    ABS_NFT = RawContract(
        title='ABS',
        address='0x211aa882d0f33ac04d2b5dc0926274874e9a5627',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    TY_NFT = RawContract(
        title='TY',
        address='0xc8332e02e88629698a533128766208856187cdef',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    SBS_NFT = RawContract(
        title='SBS',
        address='0x3d098fafea9cc8e1bf2315bf3e16828d551e66cb',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    DBS_NFT = RawContract(
        title='DBS',
        address='0x87f5ba5fe2217ec82ebb69e4da483af7d8e06730',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    MGB_NFT = RawContract(
        title='MGB',
        address='0x516fd179ec35c75c432aead0593d12d73f478f88',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    AST_NFT = RawContract(
        title='AST',
        address='0x78c82685d05188f96f1d207ba5e922290e9c2f48',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    HLC_NFT = RawContract(
        title='HLC',
        address='0x09de8c22be581720b807943f34cb4f3857e89b45',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    BCL_NFT = RawContract(
        title='BCL',
        address='0xb04b4e53ccb9732fd5b1b8c28c67bec637e2255e',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    BSS_NFT = RawContract(
        title='BSS',
        address='0xd4fc8ae96fbda1ff2de76f5dbf849c197d5d7a9e',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    BFR_NFT = RawContract(
        title='BFR',
        address='0x7dd3513086389cf5185b116a0a8a6ab9b7c1aa6e',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    UBS_NFT = RawContract(
        title='UBS',
        address='0xd437634777df6132b7edbb24b9147bedaf4c6b1b',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    LFS_NFT = RawContract(
        title='LFS',
        address='0x2e4c10db2328037f7600aa1efba75d49c0710cfa',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    BTM_NFT = RawContract(
        title='BTM',
        address='0x5919f40f0d3115869882eea8ce491ea33be0ff7e',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    BAS_NFT = RawContract(
        title='BASS',
        address='0x6c4e6782392296ca9411cc0629c7aff0e1a4e8e6',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    ARTB_NFT = RawContract(
        title='ARTB',
        address='0x7a2eeba72c950c41eb66e726e81ef14cde1545a5',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    NTM_NFT = RawContract(
        title='NTM',
        address='0x2337bb75a66d9a1e6d0118091562355f4e916378',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    QBS_NFT = RawContract(
        title='QBS',
        address='0xea10934dce66a071cbde9a10da7a8b7686d2cd30',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    BAZ_NFT = RawContract(
        title='BAZ',
        address='0x84f1bc9b51076d071665aae72abbf43c175d93b6',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    TIM_NFT = RawContract(
        title='TIM',
        address='0x0c51797bf18bad7923677578cfd0fd0c46696681',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    LUE_NFT = RawContract(
        title='LUE',
        address='0xbd0593ebc789449974e56f7ae45b422267e5da40',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    BLL_NFT = RawContract(
        title='BLL',
        address='0x0bbff707f38ff53be0a0c5844e3313f6e217e3fb',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    UNI_NFT = RawContract(
        title='UNI',
        address='0x5859ee0355a4f901d481385d4b6eff5d00356635',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    BSW_NFT = RawContract(
        title='BSW',
        address='0x378044e1589bfeed3547f3649f9af3c098fb8448',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    SQU_NFT = RawContract(
        title='SQU',
        address='0x27b335502f015328bc293adcb5c12d4269424548',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    BRY_NFT = RawContract(
        title='BRY',
        address='0x9d5533432c5e3852099c69660fce79f847283d19',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    PSS_NFT = RawContract(
        title='PSS',
        address='0x458ded9caa065929db4dfb43c766ab56877aba6c',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )

    DIF_NFT = RawContract(
        title='DIF',
        address='0x9436aa93346e11728f6059621657690097328eb8',
        abi=read_json(path=(ABIS_DIR, 'nft.json'))
    )
