from web3 import Web3
import json
my_provider = Web3.IPCProvider('/my/node/ipc/path')

KOVAN_ENDPOINT = 'https://kovan.infura.io/v3/b26481279d3a46afab21c568f94ce9d1'
KOVAN_ADDRESS = ''
MAINNET_ENDPOINT = ''
MAINNET_ADDRESS = ''

class InfuraClient():

    def __init__(self, network='dev'):
        if network == 'dev':
            infura_endpoint = KOVAN_ENDPOINT
            contract_address = KOVAN_ADDRESS
        if network == 'prod':
            infura_endpoint = MAINNET_ENDPOINT
            contract_address = MAINNET_ADDRESS
        self.web3 = Web3(Web3.HTTPProvider(infura_endpoint, request_kwargs={'timeout': 600}))
        with open('contract_abi.json') as f:
            abi_string = f.read()
        contract_abi = json.loads(abi_string)
        self.contract = self.web3.eth.contract(
            address=contract_address,
            abi=contract_abi,
        )

    def run(self):
        pass


var Web3 = require('web3')
var request = require('request');
var contract = require('truffle-contract')
var zastrin_pay_artifacts = require('./build/contracts/ZastrinPay.json')
var ws_provider = 'wss://mainnet.infura.io/ws'
var web3 = new Web3(new Web3.providers.WebsocketProvider(ws_provider))
var ZastrinPay = contract(zastrin_pay_artifacts);
var econtract = new web3.eth.Contract(ZastrinPay.abi, '<address>');

console.log("Starting listner ....");

newPaymentEvent = econtract.events.NewPayment({fromBlock: 5424000, address: '<address>', toBlock: 'latest'}, function(error, result){
  if (result !== undefined) {
    var args = result.returnValues;
    args["_txn"] = result.transactionHash;
    console.log(args);
  }
});