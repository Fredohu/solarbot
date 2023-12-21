import os
import requests
from solana.rpc.api import Client
from solana.publickey import Pubkey  # Add this line
from theblockchainapi import TheBlockchainAPIResource, SolanaNetwork


class SolEnd:
    def __init__(self):
        self.addr_to_nick = {}
        self.BLOCKCHAIN_API_RESOURCE = TheBlockchainAPIResource(
            api_key_id="abASrcTWrD98frf"
            ,
            api_secret_key="BNw0FwYS56mEQCo"
        )
        self.users_profile = {}

    def connect(self):
        server = "https://api.devnet.solana.com/"
        client = Client(server)
        return client

    def balance(self, address, client):
    pubkey = Pubkey(address)
    return client.get_balance(pubkey)

    def price_in_usdt(self):
        link_sol = 'https://public-api.solscan.io/market/token/So11111111111111111111111111111111111111112'
        res = requests.get(link_sol).json()
        return res["priceUsdt"]

    def registration(self, pub_key, nickname):
        self.addr_to_nick[nickname] = pub_key
        return self.addr_to_nick

    def get_tokens(self, address):
    address_of_tokens = []
    try:
        res = requests.get(f'https://api-devnet.solscan.io/account/tokens?address={address}').json()
        data = res.get('data', [])
        for tokens in data:
            address_of_tokens.append(tokens['tokenAddress'])
        print(address_of_tokens)
        return address_of_tokens
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return []

    def get_nft_metadata(self, nft_address):
        nft_metadata = self.BLOCKCHAIN_API_RESOURCE.get_nft_metadata(
            mint_address=nft_address,
            network=SolanaNetwork.DEVNET
        )
        return nft_metadata

    def get_uri_token(self, nft_metadata):
        uri_token = nft_metadata['data']['uri']
        return uri_token

    def request_img(self, uri_token):
        img = requests.get(uri_token).json()['image']
        return img

    def request_data(seld, uri_token):
        name = requests.get(uri_token).json()["name"]
        info = requests.get(uri_token).json()["description"]
        fin = name + '\n' + info + '\n' + "price is not set now, you can offer it"
        return fin 
    
    def bind(self, binder, holder, nft_address):
        self.users_profile[holder] = {"token": nft_address,
        "binder": binder}
if __name__ == "__main__":
    address = 'H2hFezqB6JNVUixUMttJogFr3KvhTDX4bLvT8Rq4eJwW'
    print(SolEnd().req(address))
