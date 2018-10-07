from web3 import Web3
import json
import time
import websockets
import asyncio
import os
from TeamModel import TeamModel

KOVAN_ENDPOINT = 'wss://kovan.infura.io/ws'
KOVAN_ADDRESS = '0xc42E75b377e887E39A9Ab596D50edeb1F2778c81'
MAINNET_ENDPOINT = 'wss://mainnet.infura.io/ws'
MAINNET_ADDRESS = '0xc42E75b377e887E39A9Ab596D50edeb1F2778c81'

CREATE_TEAM_TOPIC = '0x8c81f692c9063a2d41e52e0ea8b183d8585dac2d263243e2fa7695727b52f0f1'
BET_TOPIC = '0xca49f418dd97ad76b84ed6fb8e915ecccb519c5379cf6a4a455c2be7618fda2f'

class InfuraClient():

    def __init__(self, network='dev'):
        if network == 'dev':
            self.infura_endpoint = KOVAN_ENDPOINT
            self.contract_address = KOVAN_ADDRESS
        if network == 'prod':
            self.infura_endpoint = MAINNET_ENDPOINT
            self.contract_address = MAINNET_ADDRESS
        self.web3 = Web3(Web3.WebsocketProvider(self.infura_endpoint))
        with open('contract_abi.json') as f:
            abi_string = f.read()
        contract_abi = json.loads(abi_string)
        self.contract = self.web3.eth.contract(
            address=self.contract_address,
            abi=contract_abi,
        )
        os.environ['stage'] = network

    async def get_event(self):
        async with websockets.connect(self.infura_endpoint) as websocket:
            request_data = {
                'jsonrpc': '2.0',
                'method': 'eth_newFilter',
                'params':[
                    {
                        'topics': [[CREATE_TEAM_TOPIC, BET_TOPIC]]
                    }
                ],
                'id': 1
            }
            await websocket.send(json.dumps(request_data))
            response = await websocket.recv()
            filter_id = json.loads(response)['result']
            print(filter_id)

            request_data = {'jsonrpc': '2.0', 'method': 'eth_getFilterChanges', 'params': [filter_id], 'id': 1}

            while(True):
                await websocket.send(json.dumps(request_data))
                response = await websocket.recv()
                # response = '{"jsonrpc":"2.0","id":1,"result":[{"address":"0xc42e75b377e887e39a9ab596d50edeb1f2778c81","blockHash":"0xe5959103564eb936bb3527abdda178b678a85938cc96ed9290ce67afa1ab84fa","blockNumber":"0x62b817","data":"0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000cecb01659ef27a5b29ef1c0e4e268269be13318900000000000000000000000000000000000000000000000000005af3107a4000","logIndex":"0x5d","removed":false,"topics":["0xca49f418dd97ad76b84ed6fb8e915ecccb519c5379cf6a4a455c2be7618fda2f"],"transactionHash":"0xbefccf1176ff45eb97eba8a3808791d63dca0b84f720a8fff5d487d87308f930","transactionIndex":"0x68"}]}'
                data_json = json.loads(response)
                new_events = data_json['result']
                print(response)
                for new_event in new_events:
                    tx_hash = new_event['transactionHash']
                    hex_data = new_event['data']
                    raw_hex = hex_data.split('0x')[1]
                    topics = new_event['topics']
                    if CREATE_TEAM_TOPIC in topics:
                        team_id = int(raw_hex[64*0:64*1], 16)
                        submitter_address = '0x' + raw_hex[64*1:64*2][-40:]
                        arg3 = int(raw_hex[64*2:64*3], 16)
                        arg4 = int(raw_hex[64*3:64*4], 16)
                        team_name = bytearray.fromhex(raw_hex[64*4:64*5]).decode()
                        print('topic was found!')
                        print(raw_hex)
                        print(team_id, submitter_address, arg3, arg4, team_name)
                        try:
                            team = TeamModel.get(tx_hash)
                            team.team_id = team_id
                            team.address = submitter_address
                            team.mined = True
                            team.save()
                        except:
                            new_team = TeamModel(
                                tx_hash,
                                address=submitter_address,
                                name=team_name,
                                team_id=team_id,
                                mined=True,
                            )
                            new_team.save()
                    if BET_TOPIC in topics:
                        team_id = int(raw_hex[64*0:64*1], 16)
                        submitter_address = '0x' + raw_hex[64*1:64*2][-40:]
                        wei_amount = self.web3.fromWei(int(raw_hex[64*2:64*3], 16), 'ether')
                        team_on_chain = self.contract.functions.teamInfo(team_id).call()
                        print(team_id, submitter_address, wei_amount)
                        print(team_on_chain)
                        team = list(TeamModel.team_id_index.query(team_id))[0]
                        team.address = team_on_chain[0]
                        team.total_staked_ether = float(self.web3.fromWei(team_on_chain[2], 'ether'))
                        team.total_bets_made = team_on_chain[3]
                        team.save()
                
                time.sleep(15)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.get_event())


