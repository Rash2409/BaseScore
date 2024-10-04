# BaseScore

## Функционал софта

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

1. **Установка Python:**
   Скачайте и установите Python 3.11: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Установка PyCharm (рекомендуется):**
   Скачайте и установите PyCharm Community Edition: [https://www.jetbrains.com/pycharm/download/?section=windows](https://www.jetbrains.com/pycharm/download/?section=windows)

3. **Клонирование репозитория:**
```bash
git clone https://github.com/Rash2409/BaseScore.git
```

4. **Создание и активация виртуального окружения:**
```bash
py -m venv .venv
.venv\Scripts\activate
```
5. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```
6. **Создание папки files:**
```bash
python app.py
```
Выберите опцию 4 в меню.

7. **Настройка import.csv:**
Откройте файл import.csv в папке files и добавьте ваши приватные ключи и прокси в формате:

private_key,proxy
0x...,http://login:password@ip:port
0x...,http://login:password@ip:port
...

8. **Добавление кошельков:**
```bash
python app.py
```
Выберите опцию 1.

9. **Установка DB Browser for SQLite (для просмотра базы данных):**
https://sqlitebrowser.org/dl/

10. **Настройка settings.json:**
Откройте settings.json в папке files и настройте следующие параметры:

* maximum_gas_price: Максимальная цена газа.

* okx: Настройки для OKX (API ключ, секретный ключ, секретная фраза). ВАЖНО: Добавьте адреса кошельков в адресную книгу OKX и верифицируйте их. При выводе с OKX автоматически отправляется 0.00105 ETH в сеть Arbitrum (для бриджа USDC).

* withdraw_amount: Количество ETH для вывода (МИН(желательный минимум 0.0035)МАКС).

* delay_between_withdrawals: Задержка между выводами (в секундах).

* credentials: Ваши данные для работы с биржей (API, секретный ключ, секретная фраза). Пример как их получить: https://www.youtube.com/watch?v=vl6VujTLZVQ

* initial_actions_delay: Задержка между действиями аккаунтов (в секундах).

* eth_amount_for_swap: Количество ETH для свапа (МИН(желательный минимум 0.0026)МАКС).

* eth_amount_for_aave: Количество ETH для депозита в Aave.

11. **Запуск софта:**
```bash
python app.py
```
Выберите опцию 3 (вывод с OKX) или 2 (запуск основных функций).

## Если вы нашли ошибку(и):
Телеграм канал: https://t.me/+xysQ1BFueioyNmMy

Чат: https://t.me/+n_C6p-5rEGszZGNi

Личка: @nofomo_manager









```bash
py -m venv .venv
```