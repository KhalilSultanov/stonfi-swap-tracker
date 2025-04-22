# 🚀 TON STON.fi Swap Parser

Тестовое задание реализующее парсинг и сохранение swap-транзакций с кошельков блокчейна TON, совершённых через
DEX-контракт [STON.fi](https://ston.fi).

## Стэк проекта

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Docker**

## Функционал

Сервис предоставляет 2 API-ручки:

- **POST `/parse-swaps`**
    - Принимает адрес TON-кошелька.
    - Ищет и сохраняет swap-транзакции через STON.fi DEX.
    - Возвращает список новых транзакций.

- **GET `/swaps`**
    - Возвращает сохранённые swap-транзакции по адресу кошелька и диапазону дат.
    - Даты необязательны (по умолчанию последние 30 дней).

## Запуск приложения

### 1. Клонируй репозиторий

```bash
  git clone https://github.com/KhalilSultanov/stonfi-swap-tracker.git
  cd stonfi-swap-tracker
```

### 2. Создай файл `.env`

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=swap_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

TONAPI_KEY=your_tonapi_key
TONAPI_BASE_URL=https://tonapi.io/v2/blockchain/accounts
STONFI_CONTRACT_MAINNET=EQB3ncyBUTjZUA5EnFKR5_EnOMI9V1tTEAAPaiU71gc4TiUt
```

Ключи для доступа к TonAPI можно получить тут → [tonconsole.com](https://tonconsole.com)

### 3. Запусти проект через Docker Compose

```bash
  docker-compose up --build
```

Сервис будет доступен по адресу:  
`http://localhost:8000`

Документация API (Swagger):  
`http://localhost:8000/docs`

## Примеры запросов

### Парсинг swap-транзакций

**POST `/parse-swaps`**

```json
{
  "wallet_address": "UQBhwXHq0pHzIJLpsdXs1pcYgh9FVQIqE_T3yOSofhjM5XzE"
}
```

Ответ:

```json
[
  {
    "id": 1,
    "wallet_address": "UQBhwXHq0pHzIJLpsdXs1pcYgh9FVQIqE_T3yOSofhjM5XzE",
    "tx_hash": "123abc...",
    "token_in": "token_wallet_address",
    "token_out": "destination_address",
    "amount_in": 10.0,
    "amount_out": 9.8,
    "timestamp": "2025-04-22T14:52:00",
    "status": "success"
  }
]
```

### Получение транзакций из БД

**GET `/swaps`**

```
/swaps?wallet_address=UQBhwXHq0pHzIJLpsdXs1pcYgh9FVQIqE_T3yOSofhjM5XzE&from_date=2024-12-01&to_date=2025-01-01
```

Ответ:

```json
[
  {
    "id": 1,
    "wallet_address": "UQBhwXHq0pHzIJLpsdXs1pcYgh9FVQIqE_T3yOSofhjM5XzE",
    "tx_hash": "123abc...",
    "token_in": "token_wallet_address",
    "token_out": "destination_address",
    "amount_in": 10.0,
    "amount_out": 9.8,
    "timestamp": "2024-12-15T14:52:00",
    "status": "success"
  }
]
```