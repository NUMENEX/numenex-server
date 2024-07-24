from pydantic import BaseModel
from communex.client import CommuneClient
from communex._common import get_node_url
from .exceptions import UnauthorizedException
import re
import sr25519

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

    def verify_participant(
        self, address: str, type: str, signature: str, message: str
    ) -> bool:
        """
        Verifies if a given address is a valid miner address
        """
        verified = sr25519.verify(signature, message, address)
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
        if type == "miner":
            if address not in miners:
                raise UnauthorizedException("Miner not registered in subnet")
        elif type == "validator":
            if address not in validators:
                raise UnauthorizedException("Validator not registered in subnet")

    def extract_address(self, string: str):
        return re.search(IP_REGEX, string)
