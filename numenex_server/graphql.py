from pydantic import BaseModel
from typing import Optional, Dict
import requests
from fastapi import HTTPException
import logging


class UniswapGraphqlConfig(BaseModel):
    graphql_url: str
    api_key: str
    token_addresses: str


class UniswapV3Graphql:
    def __init__(self, config: UniswapGraphqlConfig) -> None:
        self.config = config

    def get_swap_details(self, hash: str):
        api_key = self.config.api_key
        subgraph_url = self.config.graphql_url
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        query = """
            query Swaps($hash: String!) {
            swaps(
                subgraphError: allow
                where: {
                transaction: $hash
                }
            ) {
                id
                timestamp
                sender
                recipient
                origin
                amount0
                amount1
                amountUSD
                sqrtPriceX96
                tick
                logIndex
                token0 {
                    id
                    name
                    symbol
                }
                token1 {
                    id
                    name
                    symbol
                }
            }
            }
            """
        # Prepare the request payload
        payload = {"query": query}
        variables = {"hash": hash}
        if variables:
            payload["variables"] = variables

        # Send the GraphQL request to the Subgraph
        response = requests.post(subgraph_url, headers=headers, json=payload)

        # Check if the request was successful
        try:
            if response.status_code == 200:
                swap_data = response.json()
                if len(swap_data["data"]["swaps"]) > 0:
                    return swap_data["data"]["swaps"]
                else:
                    raise HTTPException(status_code=400, detail="Transaction not found")
            else:
                raise HTTPException(status_code=400, detail="Unexpected Error Occured")
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=e.detail or "Unexpected Error Occured"
            )
