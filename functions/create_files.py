import os
import csv

from libs.eth_async.utils.utils import update_dict
from libs.eth_async.utils.files import touch, write_json, read_json

from data import config
from data.models import WalletCSV


def create_files():
    touch(path=config.FILES_DIR)
    touch(path=config.LOG_FILE, file=True)
    touch(path=config.ERRORS_FILE, file=True)

    if not os.path.exists(config.IMPORT_FILE):
        with open(config.IMPORT_FILE, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(WalletCSV.header)

    try:
        current_settings: dict | None = read_json(path=config.SETTINGS_FILE)
    except Exception:
        current_settings = {}

    settings = {
        'maximum_gas_price': 40,
        'okx': {
            'withdraw_amount': {'from': 0.006, 'to': 0.007},
            'delay_between_withdrawals': {'from': 1200, 'to': 1500},
            'credentials': {
                'api_key': '',
                'secret_key': '',
                'passphrase': '',
            }
        },
        'initial_actions_delay': {'from': 3600, 'to': 14400},
        'eth_amount_for_swap': {'from': 0.0001, 'to': 0.0008},
        'eth_amount_for_aave': {'from': 0.0001, 'to': 0.0008},
    }
    write_json(path=config.SETTINGS_FILE, obj=update_dict(modifiable=current_settings, template=settings), indent=2)


create_files()
