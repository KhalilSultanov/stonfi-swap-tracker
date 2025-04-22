# TON STON.fi Swap Parser

Простой и надёжный сервис для парсинга и сохранения swap-транзакций с кошельков блокчейна TON, совершённых через
DEX-контракт [STON.fi](https://ston.fi).

## Технологии

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL** (Docker)
- **Alembic** (миграции)
- **TON SDK**
- **Docker Compose**

## Функционал

Сервис предоставляет 2 API-ручки:

- \*\*POST \*\***`/parse-swaps`**

    - Принимает адрес TON-кошелька.
    - Ищет и сохраняет swap-транзакции через STON.fi DEX.
    - Возвращает список новых транзакций.

- \*\*GET \*\***`/swaps`**

    - Возвращает сохранённые swap-транзакции по адресу кошелька и диапазону дат.
    - Даты необязательны (по умолчанию последние 30 дней).

---

## Запуск приложения

### 1. Клонируй репозиторий

```bash
  git clone https://github.com/your_username/ton-stonfi-parser.git
  cd ton-stonfi-parser
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

Ключи для доступа к TonAPI можно получить на [tonconsole.com](https://tonconsole.com)

### 3. Запусти всё приложение

```bash
  docker-compose up --build
```

Проект будет доступен по адресу: `http://localhost:8000`\
Документация: `http://localhost:8000/docs`

---

## Примеры запросов

### POST `/parse-swaps`

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

### GET `/swaps`

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