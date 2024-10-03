# BaseScore

## Функцонал софта

Софт предназначен для повышения вашего Score в сети Base:

* Поддержка прокси
* Поддержка работы с базой данных
* Асинхронный ООП код
* Газ чекер
* Поддерживает вывод с OKX
* Сохранение процесса для аккаунтов в базе данных
* Делает свапы в Uniswap | SwapBased | Aerodrom
* Деплоит контракт в Owlto
* Делает bridge USDC в сеть Arbitrum и обратно в Base
* Депозитит Eth в лендинг Aave
* Минтит 30 разных NFT

## Инструкция к запуску

* Скачиваем Phyton 3.11 - https://www.python.org/downloads/
* Скачиваем Pycharm(Community Edition) - https://www.jetbrains.com/pycharm/download/?section=windows

* Скачиваем файл или же клонируем репозиторий ниже
```bash
git clone https://github.com/Rash2409/BaseScore.git
```

* Далее открываем проект в Pycharm и открываем файл BaseScore



* Устанавливаем зависимости в терминале
```bash
pip install -r requirements.txt
```

* Запускаем проект
```bash
python app.py
```

* После этого вам необходимо нажать 4, чтобы вы увидели, что создалась папка files
* Необходимо в этой папке найти файл import.csv и туда завести ваши приватные ключи от кошельков и прокси
* После этого еще раз выполняете команду - python app.py и нажимаете кнопку 1, чтобы добавить кошельки
* Перед запуском софта, перейдите в папку files в файл settings. Ниже написано, что выполняет каждый пункт

* maximum_gas_price - максимальный допустимый газ, при котором будут выполняться ваши транзакции 

* okx - настройки по выводу с биржи

* ❗❗❗ВАЖНО❗❗❗:
1) Для того чтобы выводить токены с биржи, вы должны добавить в книгу адресов OKX ваши кошельки и верефицировать
2) Если вы будете использовать софт для вывода с биржи, он также автоматически будет закидывать 0,00105 ETH в сеть Arbitrum(это нужно для функции 'bridge USDC в сеть Arbitrum и обратно в Base')

* withdraw_amount - количество эфира, которые вы хотите вывести с биржи(мин(желательное миниальное значение 0,0035) и макс) | выводит в сеть Base и минимальное количество в Arbitrum

* delay_between_withdrawals - задержка между выводами в секундах(мин и макс) 

* credentials - ваши данные для работы с биржей(апи, секретный ключ и секретная фраза | пример как получить эти данные - https://www.youtube.com/watch?v=vl6VujTLZVQ)

* initial_actions_delay - задержка между действиями ваших аккаунтов в секундах(мин и макс)

* eth_amount_for_swap - количество эфира, которое будет свапать софт(мин(желательное миниальное значение 0,0026) и макс)

* eth_amount_for_aave - количество эфира, которое будет депозитить софт в лендинг(мин и макс)

* После настройки софта, можете его запустить. Еще раз выполняете команду
```bash
python app.py
```
* Нажимаете кнопку 3(если хотите вывести деньги с OKX) или 2(если хотите начать запуск софта)

## Если есть вопросы или вы нашли ошибку(и) в софте, пишите сюда

* Тг канал - https://t.me/+xysQ1BFueioyNmMy
* Чат - https://t.me/+n_C6p-5rEGszZGNi
* Личка - http://t.me/nofomo_manager
