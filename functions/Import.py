import csv
import random

from loguru import logger

from libs.eth_async.client import Client
from libs.eth_async.data.models import Networks
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data import config
from data.models import WalletCSV, Settings
from tasks.base import randfloat
from utils.db_api.models import Wallet


class Import:
    @staticmethod
    def get_wallets_from_csv(csv_path: str, skip_first_line: bool = True) -> list[WalletCSV]:
        wallets = []

        with open(csv_path) as f:
            reader = csv.reader(f)
            for row in reader:
                if skip_first_line:
                    skip_first_line = False
                    continue
                wallets.append(WalletCSV(
                    private_key=row[0],
                    proxy=row[1]
                ))
        return wallets

    @staticmethod
    async def wallets():
        settings = Settings()
        wallets = Import.get_wallets_from_csv(csv_path=config.IMPORT_FILE)

        imported = []
        edited = []
        total = len(wallets)

        # Создаем engine и Session здесь
        engine = create_engine(f'sqlite:///{config.WALLETS_DB}', echo=False,
                               connect_args={'check_same_thread': False})
        Session = sessionmaker(bind=engine)

        with Session() as session:  # Используем сессию в контекстном менеджере
            for wallet in wallets:
                print("Before update/insert")  # Добавлен вывод в консоль
                wallet_instance = session.query(Wallet).filter_by(
                    private_key=wallet.private_key).first()
                if wallet_instance and (wallet_instance.proxy != wallet.proxy):
                    wallet_instance.proxy = wallet.proxy
                    session.commit()
                    edited.append(wallet_instance)

                if not wallet_instance:
                    client = Client(private_key=wallet.private_key, network=Networks.Ethereum)
                    wallet_instance = Wallet(
                        private_key=wallet.private_key,
                        address=client.account.address,
                        proxy=wallet.proxy,
                        eth_amount_for_aave=randfloat(
                            from_=settings.eth_amount_for_aave.from_,
                            to_=settings.eth_amount_for_aave.to_,
                            step=0.001
                        ),
                    )

                    session.add(wallet_instance)
                    session.commit()
                    imported.append(wallet_instance)
                print("After commit", wallet_instance.id)  # Добавлен вывод в консоль

        logger.success(f'Done! imported wallets: {len(imported)}/{total}; '
                       f'edited wallets: {len(edited)}/{total}; total: {total}')
