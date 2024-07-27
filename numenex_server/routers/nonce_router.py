import typing as ty

from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from .. import schema
from siwe import generate_nonce


router = APIRouter(prefix="/nonce", tags=["nonce"])


@router.get("/")
async def get_nonce(request: Request):
    nonce = generate_nonce()
    print(nonce)
    request.session["nonce"] = nonce
    return PlainTextResponse(nonce)


@router.get("/session", response_model=schema.Session)
async def get_session(request: Request):
    return {
        "address": None,
        "chainId": None,
    }


@router.get("/signout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}


@router.get("/check/nonce")
async def check(request: Request):
    return request.session.get("nonce")
