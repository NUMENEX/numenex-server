import sr25519  # type: ignore
from typing import Dict, List, Tuple, Union


def _format_data(data: Union[List, Dict, Tuple, str]) -> bytes:
    """
    format data to str message
    :param data:
    :type data:
    :return:
    :rtype:
    """
    if isinstance(data, dict):
        sorted_data = sorted(data.items(), key=lambda x: x[0])
        message = "".join(str(value) for _, value in sorted_data)
    elif isinstance(data, (list, tuple)):
        message = "".join(str(value) for key, value in data)
    else:
        message = data
    return message.encode()


def verify_sign(pubkey: str, data, signature: str) -> bool:
    crypto_verify_fn = sr25519.verify
    message = _format_data(data)
    verified: bool = crypto_verify_fn(
        bytes.fromhex(signature), message, bytes.fromhex(pubkey)
    )
    if not verified:
        # Another attempt with the data wrapped, as discussed in https://github.com/polkadot-js/extension/pull/743
        # Note: As Python apps are trusted sources on its own, no need to wrap data when signing from this lib
        verified: bool = crypto_verify_fn(  # type: ignore
            bytes.fromhex(signature),
            b"<Bytes>" + message + b"</Bytes>",
            bytes.fromhex(pubkey),
        )
    return verified
