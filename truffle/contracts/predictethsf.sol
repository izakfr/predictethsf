pragma solidity ^0.4.2;
contract predictethsf {
  event NewTeam(
    uint256 _numteams,
    address _sender,
    string _teamname
  );

  event Bet(
    uint256 _teamindex,
    address _sender,
    uint256 _value
  );

  event Payout(
    address _winner,
    uint256 _value
  );

  // Define a bettor
  struct Bettor {
    address bettorAddress;
    uint256 amountBet;
  }

  // Define a team
  struct Team {
    address creator;
    string teamName;
    uint256 totalBet;
    uint256[] bettors;
    mapping(uint256 => Bettor) bettorInfo;
  }

  // Set necessary parameters
  address public owner;
  uint256 public minimumBet;
  mapping(uint256 => Team) public teamInfo;
  uint256 public numTeams = 0;
  uint256[] public teamList;

  // Deploy the contract
  function() public payable {}
  function predictethsf() public {
    owner = msg.sender;
    minimumBet = 100000000000000;
  }

  // Create a new team
  function newTeam(string _newTeamName) public {
    teamInfo[numTeams].teamName = _newTeamName;
    teamInfo[numTeams].totalBet = 0;
    teamInfo[numTeams].creator = msg.sender;
    teamList.push(numTeams);
    emit NewTeam(numTeams, msg.sender, _newTeamName);
    numTeams += 1;
  }

  // Add a new bet to a team
  function bet(uint256 _teamSelected) public payable {
    // Check that the bet is above the minimum
    require(msg.value >= minimumBet);
    require(_teamSelected < numTeams);

    // Add to the total of the team the amount bet
    teamInfo[_teamSelected].totalBet += msg.value;

    // Set the bettor information
    uint256 numBettors = teamInfo[_teamSelected].bettors.length;
    teamInfo[_teamSelected].bettorInfo[numBettors].amountBet = msg.value;
    teamInfo[_teamSelected].bettorInfo[numBettors].bettorAddress = msg.sender;

    // Add the bettor to the teams' bettor list
    teamInfo[_teamSelected].bettors.push(numBettors);
    emit Bet(_teamSelected, msg.sender, msg.value);
  }

  // Distribute prizes amongst the winners
  function distributePrizes(address[] winningTeams) public {
    require(owner == msg.sender);
    // This is a list of winners and a list of the amounts they bet
    uint256 count = 0;
    address[500] memory winningBettors;
    uint256[500] memory amountsBet;

    // This will take the value of all losers bet
    uint256 loserBet = 0;

    // This will take the value of all winners bet
    uint256 winnerBet = 0;

    // Loop through the teams who didn't win to find the total losing bet
    for (uint256 i = 0; i < teamList.length; i++) {
      bool winner = false;
      for (uint256 j = 0; j < winningTeams.length; j++) {
        if (teamInfo[i].creator == winningTeams[j]) {
          winner = true;
        }
      }
      if (winner) {
        for (uint256 k = 0; k < teamInfo[i].bettors.length; k++) {
          winningBettors[count] = teamInfo[i].bettorInfo[k].bettorAddress;
          amountsBet[count] = teamInfo[i].bettorInfo[k].amountBet;
          count += 1;
        }
        // Add the amount to the total winning bet
        winnerBet += teamInfo[i].totalBet;
      }
      else {
        // Add the amount to the total losing bet
        loserBet += teamInfo[i].totalBet;
      }
    }

    // Loop through winners, and disperse the ETH
    for (uint256 m = 0; m < count; m++) {
        // Check that the address in this fixed array is not empty
       if (winningBettors[m] != address(0)) {
          // Transfer the requisite amount of ETH to the winner
          Payout(winningBettors[m], (amountsBet[m]*(10000+(loserBet*10000/winnerBet)))/10000);
          winningBettors[m].transfer((amountsBet[m]*(10000+(loserBet*10000/winnerBet)))/10000);
       }
    }
  }

  function TeamTotalBet(uint256 _team) public view returns(uint256){
    return teamInfo[_team].totalBet;
  }

  function TeamName(uint256 _team) public view returns(string){
    return teamInfo[_team].teamName;
  }

  function TeamCreator(uint256 _team) public view returns(address){
    return teamInfo[_team].creator;
  }

  function TeamNumBettors(uint256 _team) public view returns(uint256){
    return teamInfo[_team].bettors.length;
  }
}
