import logging
from fastapi.security import SecurityScopes
from .database import Database
from fastapi import Request, HTTPException
from .commune import VerifyCommuneMinersAndValis
from .exceptions import UnauthenticatedException
from siwe import SiweMessage, siwe

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


def get_headers_data(request: Request):
    address = request.headers.get("X-address")
    signature = request.headers.get("X-signature")
    message = request.headers.get("X-message")
    return address, signature, message


def get_miner(
    request: Request,
    _: SecurityScopes,
):
    address, signature, message = get_headers_data(request)

    if (address or signature or message) is None:
        raise UnauthenticatedException
    request.state.commune_verifier.verify_participant(
        address, "miner", signature, message
    )
    return address


def get_validator(
    request: Request,
    _: SecurityScopes,
):
    address, signature, message = get_headers_data(request)

    if (address or signature or message) is None:
        raise UnauthenticatedException
    request.state.commune_verifier.verify_participant(
        address, "validator", signature, message
    )
    return address


def get_siwe_msg(
    request: Request,
    _: SecurityScopes,
):
    signature, message = get_headers_data(request)
    if (signature or message) is None:
        raise UnauthenticatedException
    try:
        siwe_msg = SiweMessage.from_message(message=message)
        siwe_msg.verify(signature=signature)
        if siwe_msg.chain_id != "56":
            raise HTTPException(status_code=400, detail="Invalid chain")
        if siwe_msg.nonce != request.session.get("nonce"):
            raise HTTPException(status_code=400, detail="Nonce mismatch")
        request.session.clear()
        return siwe_msg, message
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
