from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = 'wallets_mm'

    id: Mapped[int] = mapped_column(primary_key=True)
    private_key: Mapped[str] = mapped_column(unique=True, index=True)
    address: Mapped[str]
    proxy: Mapped[str]
    aave_depozit: Mapped[bool] = mapped_column(default=False, server_default='0')
    aave_withdraw: Mapped[bool] = mapped_column(default=False, server_default='0')
    eth_amount_for_aave: Mapped[int]
    next_initial_action_time: Mapped[datetime | None] = mapped_column(default=None)
    initial_completed: Mapped[bool] = mapped_column(default=False, server_default='0')
    completed: Mapped[bool] = mapped_column(default=False, server_default='0')

    zorb_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    spg_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    dst_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    abs_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    ty_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    sbs_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    dbs_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    mgb_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    ast_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    hlc_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    bcl_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    bss_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    bfr_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    ubs_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    lfs_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    btm_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    bas_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    artb_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    ntm_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    qbs_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    baz_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    tim_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    lue_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    bll_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    uni_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    bsw_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    squ_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    bry_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    pss_nft: Mapped[bool] = mapped_column(default=False, server_default='0')
    dif_nft: Mapped[bool] = mapped_column(default=False, server_default='0')

    def __repr__(self):
        return f'{self.address}'
