from solana.rpc.api import Client
from theblockchainapi import TheBlockchainAPIResource, SolanaNetwork
import requests
import json


class SolEnd:
    def __init__(self):
        self.addr_to_nick = {}
        self.BLOCKCHAIN_API_RESOURCE = TheBlockchainAPIResource(
            api_key_id=""
            ,
            api_secret_key=""
        )
        self.users_profile = {}

    def connect(self):
        server = "https://solana-mainnet.phantom.tech"
        client = Client(server)
        return client

    def balance(self, address, client):
        return client.get_balance(address)

    def price_in_usdt(self):
        link_sol = 'https://public-api.solscan.io/market/token/So11111111111111111111111111111111111111112'
        res = requests.get(link_sol).json()
        return res["priceUsdt"]

    def registration(self, pub_key, nickname):
        self.addr_to_nick[nickname] = pub_key
        return self.addr_to_nick

    def get_tokens(self, address):
        address_of_tokens = []
        link = f'https://public-api.solscan.io/account/tokens?account={address}'
        res = requests.get(link).json()

        for tokens in res:
            address_of_tokens.append(tokens['tokenAddress'])
        print(address_of_tokens)
        return address_of_tokens

    def get_nft_metadata(self, nft_address):
        nft_metadata = self.BLOCKCHAIN_API_RESOURCE.get_nft_metadata(
            mint_address=nft_address,
            network=SolanaNetwork.MAINNET_BETA
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
