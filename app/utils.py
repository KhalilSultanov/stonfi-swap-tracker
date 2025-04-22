import backoff
import requests

from app.config import settings


@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.RequestException,),
    max_tries=5,
    jitter=backoff.full_jitter
)
def fetch_transactions(wallet_raw: str):
    response = requests.get(
        f"{settings.TONAPI_BASE_URL}/{wallet_raw}/transactions",
        params={"limit": 50},
        headers={"Authorization": f"Bearer {settings.TONAPI_KEY}"},
        timeout=10
    )
    response.raise_for_status()
    return response.json()
