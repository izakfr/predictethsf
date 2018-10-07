var abi = [
  {
    "constant": true,
    "inputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "teamInfo",
    "outputs": [
      {
        "name": "creator",
        "type": "address"
      },
      {
        "name": "teamName",
        "type": "string"
      },
      {
        "name": "totalBet",
        "type": "uint256"
      },
      {
        "name": "numBettors",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "minimumBet",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "numTeams",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "payable": true,
    "stateMutability": "payable",
    "type": "fallback"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "_numteams",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_sender",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "_teamname",
        "type": "string"
      }
    ],
    "name": "NewTeam",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "_teamindex",
        "type": "uint256"
      },
      {
        "indexed": false,
        "name": "_sender",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "_value",
        "type": "uint256"
      }
    ],
    "name": "Bet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "name": "_winner",
        "type": "address"
      },
      {
        "indexed": false,
        "name": "_value",
        "type": "uint256"
      }
    ],
    "name": "Payout",
    "type": "event"
  },
  {
    "constant": false,
    "inputs": [],
    "name": "kill",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_newTeamName",
        "type": "string"
      }
    ],
    "name": "newTeam",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "_teamSelected",
        "type": "uint256"
      }
    ],
    "name": "bet",
    "outputs": [],
    "payable": true,
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "winningTeams",
        "type": "uint256[]"
      }
    ],
    "name": "distributePrizes",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_team",
        "type": "uint256"
      }
    ],
    "name": "TeamTotalBet",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_team",
        "type": "uint256"
      }
    ],
    "name": "TeamName",
    "outputs": [
      {
        "name": "",
        "type": "string"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_team",
        "type": "uint256"
      }
    ],
    "name": "TeamCreator",
    "outputs": [
      {
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "_team",
        "type": "uint256"
      }
    ],
    "name": "TeamNumBettors",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }]

function bet(teamIndex, amountBetting) {
  if (window.ethereum) {
    window.web3 = new Web3(ethereum);

    // Load contract and address
    var predictethsf = web3.eth.contract(abi);
    var instance = predictethsf.at('0xFFe506aB67a5D7e96e8C4a25F6BE93F89020cc88')
    var address = web3.eth.accounts[0];
    var val = window.web3.toWei(amountBetting, 'ether');
    instance.bet(teamIndex, {from: address, value: val}, function(error, result){
      if(error) {
        return false;
        console.log(error)
      }
    });
    return true;
  }
  else {
    window.web3 = new Web3(web3.currentProvider);

    // Load contract and address
    var predictethsf = web3.eth.contract(abi);
    var instance = predictethsf.at('0xFFe506aB67a5D7e96e8C4a25F6BE93F89020cc88');
    var address = web3.eth.accounts[0];
    var val = window.web3.toWei(amountBetting, 'ether');
    instance.bet(teamIndex, {from: address, value: val}, function(error, result){
      if(error) {
        return false;
        console.log(error)
      }
    });
    return true;
  }
}
