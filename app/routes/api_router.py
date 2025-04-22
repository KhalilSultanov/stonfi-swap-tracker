from datetime import datetime, timedelta

import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.db import get_db
from app.schemas import WalletAddressSchema, SwapTransactionOut
from tonsdk.utils import Address

from app.utils import fetch_transactions

api_router = APIRouter()

STONFI_CONTRACT_RAW = Address(settings.STONFI_CONTRACT_MAINNET).to_string(False)


@api_router.post("/parse-swaps", response_model=list[SwapTransactionOut])
def parse_swaps(payload: WalletAddressSchema, db: Session = Depends(get_db)):
    try:
        wallet_raw = Address(payload.wallet_address).to_string(False)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid wallet address format")

    try:
        data = fetch_transactions(wallet_raw)
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="TonAPI unavailable")

    transactions = data.get("transactions", [])
    swap_txs = []

    for tx in transactions:
        if not tx.get("success"):
            continue

        in_msg = tx.get("in_msg", {})
        out_msgs = tx.get("out_msgs", [])
        tx_hash = tx.get("hash")
        timestamp = tx.get("utime")

        involved = (
                in_msg.get("destination", {}).get("address") == STONFI_CONTRACT_RAW or
                any(msg.get("destination", {}).get("address") == STONFI_CONTRACT_RAW for msg in out_msgs)
        )

        if not involved:
            continue

        decoded = in_msg.get("decoded_body", {})
        payload_val = decoded.get("forward_payload", {}).get("value", {})

        if (
                in_msg.get("decoded_op_name") != "jetton_notify" or
                payload_val.get("sum_type") != "StonfiSwap"
        ):
            continue

        swap_data = payload_val.get("value", {})
        token_wallet = swap_data.get("token_wallet")
        min_out = int(swap_data.get("min_out", 0)) / 1e9
        to_address = swap_data.get("to_address")
        amount_in = int(decoded.get("amount", 0)) / 1e9

        tx_obj = models.SwapTransaction(
            wallet_address=payload.wallet_address,
            tx_hash=tx_hash,
            token_in=token_wallet,
            token_out=to_address,
            amount_in=amount_in,
            amount_out=min_out,
            timestamp=datetime.utcfromtimestamp(timestamp),
            status="success"
        )

        if not db.query(models.SwapTransaction).filter_by(tx_hash=tx_hash).first():
            db.add(tx_obj)
            db.commit()
            db.refresh(tx_obj)
            swap_txs.append(tx_obj)

    return swap_txs


@api_router.get("/swaps", response_model=list[SwapTransactionOut])
def get_swaps(
        wallet_address: str,
        from_date: str = Query(default=(datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")),
        to_date: str = Query(default=datetime.utcnow().strftime("%Y-%m-%d")),
        db: Session = Depends(get_db)
):
    try:
        from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        to_dt = datetime.strptime(to_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD")

    query = db.query(models.SwapTransaction).filter(
        models.SwapTransaction.wallet_address == wallet_address,
        models.SwapTransaction.timestamp >= from_dt,
        models.SwapTransaction.timestamp <= to_dt
    )

    return query.order_by(models.SwapTransaction.timestamp.desc()).all()
