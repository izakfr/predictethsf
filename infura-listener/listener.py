from web3 import Web3
import json
import time
import websockets
import asyncio
import os
from TeamModel import TeamModel

# KOVAN_ENDPOINT = 'https://kovan.infura.io/v3/b26481279d3a46afab21c568f94ce9d1'
KOVAN_ENDPOINT = 'wss://kovan.infura.io/ws'
KOVAN_ADDRESS = '0xf4B36e5Da66917A319243D4F09BFa946588E5DFa'
MAINNET_ENDPOINT = ''
MAINNET_ADDRESS = ''

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
                # response = '{"jsonrpc":"2.0","id":1,"result":[{"address":"0xb4b0cbfdcafb60755a143d21851d7aed3a6feffe","blockHash":"0x88e7acec025d8da20311f043fdc8cd67c86110bf693688724610bc7baa71b29a","blockNumber":"0x891d59","data":"0x00000000000000000000000000000000000000000000000000000000000000010000000000000000000000002cb708306c2d60e42af951a155be0cabd5b16676000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000057465616d31000000000000000000000000000000000000000000000000000000","logIndex":"0x0","removed":false,"topics":["0x8c81f692c9063a2d41e52e0ea8b183d8585dac2d263243e2fa7695727b52f0f1"],"transactionHash":"0x85a947f941a0acc9eef87429465b243dae8b40eb77416f8dc89384fb7bba21ce","transactionIndex":"0x0","transactionLogIndex":"0x0","type":"mined"}]}'
                # response = '{"jsonrpc":"2.0","id":1,"result":[{"address":"0xb4b0cbfdcafb60755a143d21851d7aed3a6feffe","blockHash":"0xa8d8d7e25fccbd5e80282f2cbdcd1dedae15c3a0e3d7b4ab89f06bc0c0631aa2","blockNumber":"0x892183","data":"0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000002cb708306c2d60e42af951a155be0cabd5b1667600000000000000000000000000000000000000000000000000038d7ea4c68000","logIndex":"0x0","removed":false,"topics":["0xca49f418dd97ad76b84ed6fb8e915ecccb519c5379cf6a4a455c2be7618fda2f"],"transactionHash":"0xd831e2be1f048c83f4b8b59ec81b0a06e47234ee7ba0bf58b93288f79c5d8a95","transactionIndex":"0x1","transactionLogIndex":"0x0","type":"mined"}]}'
                data_json = json.loads(response)
                new_events = data_json['result']
                print(response)
                for new_event in new_events:
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
                            team = TeamModel.get(team_id)
                            team.mined = True
                            team.save()
                        except:
                            new_team = TeamModel(
                                team_id,
                                address=submitter_address,
                                name=team_name,
                            )
                            new_team.save()
                    if BET_TOPIC in topics:
                        team_id = int(raw_hex[64*0:64*1], 16)
                        submitter_address = '0x' + raw_hex[64*1:64*2][-40:]
                        wei_amount = self.web3.fromWei(int(raw_hex[64*2:64*3], 16), 'ether')
                        team_on_chain = self.contract.functions.teamInfo(team_id).call()
                        print(team_id, submitter_address, wei_amount)
                        team = TeamModel.get(team_id)
                        team.submitter_address = team_on_chain[0]
                        team.total_staked_ether = float(self.web3.fromWei(team_on_chain[2], 'ether'))
                        team.save()

                time.sleep(15)

    def run(self):
        # print(self.web3.eth.blockNumber)
        asyncio.get_event_loop().run_until_complete(self.get_event())


        # response = requests.post(self.infura_endpoint,
        #     json={
        #         'jsonrpc': '2.0',
        #         'method': 'eth_newBlockFilter',
        #         'params': [],
        #         'id': 1
        #     }
        # )
        # print(response)
        # while(True):
        #     response = requests.post(self.infura_endpoint,
        #         json={
        #             'jsonrpc': '2.0',
        #             'method': 'eth_getFilterChanges',
        #             'params': [],
        #             'id': 1
        #         }
        #     )
        #     print(response)
        #     time.sleep(5)

# async def get_eth_blockNumber(uri):
#     async with websockets.connect(uri) as websocket:
#         request_data = {'jsonrpc': '2.0', 'method': 'eth_blockNumber', 'params': [], 'id': 1}
#         await websocket.send(json.dumps(request_data))

#         result = await websocket.recv()
#         print(result)


# var Web3 = require('web3')
# var request = require('request');
# var contract = require('truffle-contract')
# var zastrin_pay_artifacts = require('./build/contracts/ZastrinPay.json')
# var ws_provider = 'wss://mainnet.infura.io/ws'
# var web3 = new Web3(new Web3.providers.WebsocketProvider(ws_provider))
# var ZastrinPay = contract(zastrin_pay_artifacts);
# var econtract = new web3.eth.Contract(ZastrinPay.abi, '<address>');

# console.log('Starting listner ....');

# newPaymentEvent = econtract.events.NewPayment({fromBlock: 5424000, address: '<address>', toBlock: 'latest'}, function(error, result){
#   if (result !== undefined) {
#     var args = result.returnValues;
#     args['_txn'] = result.transactionHash;
#     console.log(args);
#   }
# });