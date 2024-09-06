# encoding: utf-8

from fastapi import Path, HTTPException
from pydantic import BaseModel

from server import app, kaspad_client


class BalanceResponse(BaseModel):
    address: str = "brics:qqehcree82854tlnqapnn359yj9p9rchq78z5jaq5va85juaj0phg7k502mmg"
    balance: int = 38240000000


@app.get("/addresses/{bricsAddress}/balance", response_model=BalanceResponse, tags=["Brics addresses"])
async def get_balance_from_kaspa_address(
        bricsAddress: str = Path(
            description="Brics address as string e.g. brics:qqehcree82854tlnqapnn359yj9p9rchq78z5jaq5va85juaj0phg7k502mmg",
            regex="^brics\:[a-z0-9]{61,63}$")):
    """
    Get balance for a given brics address
    """
    resp = await kaspad_client.request("getBalanceByAddressRequest",
                                       params={
                                           "address": bricsAddress
                                       })

    try:
        resp = resp["getBalanceByAddressResponse"]
    except KeyError:
        if "getUtxosByAddressesResponse" in resp and "error" in resp["getUtxosByAddressesResponse"]:
            raise HTTPException(status_code=400, detail=resp["getUtxosByAddressesResponse"]["error"])
        else:
            raise

    try:
        balance = int(resp["balance"])

    # return 0 if address is ok, but no utxos there
    except KeyError:
        balance = 0

    return {
        "address": bricsAddress,
        "balance": balance
    }
