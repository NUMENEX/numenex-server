import typing as ty

from fastapi import APIRouter, Request
from ..dependencies import get_session, get_miner, get_validator
from .. import schema
from siwe import generate_nonce


router = APIRouter(prefix="/nonce", tags=["nonce"])


@router.get("/", response_model=schema.Nonce)
async def get_nonce(request: Request):
    nonce = generate_nonce()
    request.session["nonce"] = nonce
    return {"nonce": nonce}


@router.get("/check", response_model=schema.Nonce)
async def check_nonce(request: Request):
    return {"nonce": request.session.get("nonce")}
