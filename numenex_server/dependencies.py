import logging
from fastapi.security import SecurityScopes
from .database import Database
from fastapi import Request, HTTPException, Depends
from .commune import VerifyCommuneMinersAndValis
from .graphql import UniswapV3Graphql
from .exceptions import UnauthenticatedException
from siwe import SiweMessage, siwe
import typing as ty
import json

logger = logging.getLogger(__name__)


class DatabaseDependency:
    def __init__(self, db: Database) -> None:
        self.db = db

    def __call__(self, request: Request) -> None:
        request.state.db = self.db


def get_session(request: Request):
    yield from request.state.db.get_session()


class CommuneDependency:
    def __init__(self, commune_verifier: VerifyCommuneMinersAndValis) -> None:
        self.commune_verifier = commune_verifier

    def __call__(self, request: Request) -> None:
        request.state.commune_verifier = self.commune_verifier


class UniswapV3Dependency:
    def __init__(self, uniswap_v3_graphql: UniswapV3Graphql) -> None:
        self.uniswap_v3_graphql = uniswap_v3_graphql

    def __call__(self, request: Request) -> None:
        request.state.uniswap_v3_graphql = self.uniswap_v3_graphql


async def get_body_data(request: Request):
    req_body = await request.json()
    message = req_body["message"]
    signature = req_body["signature"]
    return signature, message


async def get_numx_participant(
    request: Request,
    _: SecurityScopes,
):
    signature = request.headers.get("signature")
    message = request.headers.get("message")

    if (signature or message) is None:
        raise UnauthenticatedException
    participant_type, ss58_address = request.state.commune_verifier.verify_participant(
        signature,
        message,
    )
    # TODO::: change to actual address
    return participant_type, ss58_address


async def get_validator(
    request: Request,
    _: SecurityScopes,
):
    signature, message = await get_body_data(request)

    if (signature or message) is None:
        raise UnauthenticatedException
    request.state.commune_verifier.verify_participant(
        # TODO::: change to actual address
        "address",
        "validator",
        signature,
        message,
    )
    # TODO::: change to actual address
    return "address"


async def get_siwe_msg(
    request: Request,
    _: SecurityScopes,
):
    signature, message = await get_body_data(request)
    if (signature or message) is None:
        raise UnauthenticatedException
    try:
        siwe_msg = SiweMessage.from_message(message=message, abnf=False)
        siwe_msg.verify(signature=signature)
        # if request.session.get("nonce") != siwe_msg.nonce:
        #     raise siwe.NonceMismatch
        if siwe_msg.chain_id != 42161:
            raise HTTPException(status_code=400, detail="Invalid chain")
        # TODO:: check nonce here, vite has problem with cookies
        return siwe_msg, message, request.state
    except siwe.NonceMismatch:
        raise HTTPException(status_code=400, detail="Nonce mismatch")
    except siwe.ExpiredMessage:
        raise HTTPException(status_code=400, detail="Expired message")
    except siwe.InvalidSignature:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except siwe.MalformedSession:
        raise HTTPException(status_code=400, detail="Session malformed")
    except siwe.DomainMismatch:
        raise HTTPException(status_code=400, detail="Domain mismatch")
    except siwe.VerificationError:
        raise HTTPException(status_code=400, detail="Verification error")
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid message")


def verify_trade():
    def dependency(siwe_details: ty.Tuple = Depends(get_siwe_msg)):
        siwe_message, message, state = siwe_details
        message = message.split("\n\n")[1]
        message = json.loads(message)
        swaps_array = state.uniswap_v3_graphql.get_swap_details(message["hash"])
        return siwe_message, message, swaps_array

    return dependency
