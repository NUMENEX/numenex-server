from pydantic import BaseModel
from communex.client import CommuneClient
from communex._common import get_node_url
from .exceptions import UnauthorizedException
import re
from .key import verify_sign

IP_REGEX = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+")


class CommuneConfig(BaseModel):
    use_testnet: bool
    netuid: str


class VerifyCommuneMinersAndValis:
    commune_client: CommuneClient

    def __init__(self, config: CommuneConfig) -> None:
        self.config = config
        self.commune_client = CommuneClient(
            get_node_url(use_testnet=self.config.use_testnet)
        )

    def verify_participant(self, signature: str, message: str) -> bool:
        """
        Verifies if a given address is a valid miner address
        """
        print(message, "message")
        pubkey = message.split(":")[0]
        ss58_address = message.split(":")[1]
        verified = verify_sign(pubkey=pubkey, data=message, signature=signature)
        if not verified:
            raise UnauthorizedException("Invalid signature")
        validators = []
        miners = []
        module_addreses = self.commune_client.query_map_key(self.config.netuid)
        module_keys = self.commune_client.query_map_address(self.config.netuid)
        filtered_addr = {
            id: self.extract_address(addr) for id, addr in module_keys.items()
        }
        for key, value in module_addreses.items():
            if filtered_addr.get(key) is None:
                validators.append(value)
            else:
                miners.append(value)
        if ss58_address in miners:
            return "miner", ss58_address
        elif ss58_address in validators:
            return "validator", ss58_address
        else:
            raise UnauthorizedException("User not registered in subnet")

    def extract_address(self, string: str):
        return re.search(IP_REGEX, string)
