pragma solidity ^0.4.24;

/**
 * @title SafeMath
 * @dev Math operations with safety checks that revert on error
 */
library SafeMath {

  /**
  * @dev Multiplies two numbers, reverts on overflow.
  */
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    // Gas optimization: this is cheaper than requiring 'a' not being zero, but the
    // benefit is lost if 'b' is also tested.
    // See: https://github.com/OpenZeppelin/openzeppelin-solidity/pull/522
    if (a == 0) {
      return 0;
    }

    uint256 c = a * b;
    require(c / a == b);

    return c;
  }

  /**
  * @dev Integer division of two numbers truncating the quotient, reverts on division by zero.
  */
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    require(b > 0); // Solidity only automatically asserts when dividing by 0
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold

    return c;
  }

  /**
  * @dev Subtracts two numbers, reverts on overflow (i.e. if subtrahend is greater than minuend).
  */
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    require(b <= a);
    uint256 c = a - b;

    return c;
  }

  /**
  * @dev Adds two numbers, reverts on overflow.
  */
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    require(c >= a);

    return c;
  }

  /**
  * @dev Divides two numbers and returns the remainder (unsigned integer modulo),
  * reverts when dividing by zero.
  */
  function mod(uint256 a, uint256 b) internal pure returns (uint256) {
    require(b != 0);
    return a % b;
  }
}

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
    uint256 numBettors;
    mapping(uint256 => Bettor) bettorInfo;
  }

  // Set necessary parameters
  address public owner;
  uint256 public minimumBet;
  mapping(uint256 => Team) public teamInfo;
  uint256 public numTeams = 0;

  // Deploy the contract
  function() public payable {}
  function predictethsf() public {
    owner = msg.sender;
    minimumBet = 100000000000000;
  }

  function kill() public {
    if(msg.sender == owner) selfdestruct(owner);
  }

  // Create a new team
  function newTeam(string _newTeamName) public {
    teamInfo[numTeams].teamName = _newTeamName;
    teamInfo[numTeams].totalBet = 0;
    teamInfo[numTeams].creator = msg.sender;
    emit NewTeam(numTeams, msg.sender, _newTeamName);
    numTeams += 1;
  }

  function changeTeamAddress(uint256 teamNumber, address _newTeamAddress) public {
    require(msg.sender == teamInfo[teamNumber].creator);
    teamInfo[teamNumber].creator = _newTeamAddress;
  }

  // Add a new bet to a team
  function bet(uint256 _teamSelected) public payable {
    // Check that the bet is above the minimum
    require(msg.value >= minimumBet);
    require(_teamSelected < numTeams);

    // Add to the total of the team the amount bet
    teamInfo[_teamSelected].totalBet += msg.value;

    // Set the bettor information
    uint256 numBettors = teamInfo[_teamSelected].numBettors;
    teamInfo[_teamSelected].bettorInfo[numBettors].amountBet = msg.value;
    teamInfo[_teamSelected].bettorInfo[numBettors].bettorAddress = msg.sender;

    // Add the bettor to the teams' bettor list
    teamInfo[_teamSelected].numBettors += 1;
    emit Bet(_teamSelected, msg.sender, msg.value);
  }

  function payoutWinners(uint256[] winningTeams, uint256 amountToWinningTeams) public {
    require(owner == msg.sender);
    for (uint256 n = 0; n < winningTeams.length; ++n) {
      Payout(teamInfo[winningTeams[n]].creator, amountToWinningTeams);
      teamInfo[winningTeams[n]].creator.transfer(amountToWinningTeams);
    }
  }

  // Distribute prizes amongst the winners
  function distributePrizes(uint256[] winningTeams) public {
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
    for (uint256 i = 0; i < numTeams; i++) {
      bool winner = false;
      for (uint256 j = 0; j < winningTeams.length; j++) {
        if (i == winningTeams[j]) {
          winner = true;
        }
      }
      if (winner) {
        for (uint256 k = 0; k < teamInfo[i].numBettors; k++) {
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
    uint256 amountToWinningTeams = SafeMath.div(winnerBet, 50);
    payoutWinners(winningTeams, amountToWinningTeams);

    // Loop through winners, and disperse the ETH
    for (uint256 m = 0; m < count; m++) {
        // Check that the address in this fixed array is not empty
       if (winningBettors[m] != address(0)) {
          // Transfer the requisite amount of ETH to the winner
          uint256 amountToPay = SafeMath.div(SafeMath.mul((100 - (2 * winningTeams.length)), amountsBet[m]*(10000+(loserBet*10000/winnerBet))/10000), 100);
          Payout(winningBettors[m], amountToPay);
          winningBettors[m].transfer(amountToPay);
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
    return teamInfo[_team].numBettors;
  }
}
