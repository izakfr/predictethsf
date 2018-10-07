const PredictEthSF = artifacts.require("predictethsf")

contract('predictethsf javascript tests', function (accounts) {
  accountZero = accounts[0];
  accountOne = accounts[1];
  accountTwo = accounts[2];
  accountThree = accounts[3];
  accountFour = accounts[4];
  accountFive = accounts[5];
  accountSix = accounts[6];
  accountSeven = accounts[7];

  it("initalize the contract with no teams", async () => {
    let instance = await PredictEthSF.new();
    let numTeams = await instance.numTeams();
    assert.equal(numTeams, 0, "initalizing with no teams failed");
  })

  it("create two teams", async () => {
    let instance = await PredictEthSF.new();
    await instance.newTeam("zero");
    let numTeams_one = await instance.numTeams();
    await instance.newTeam("one");
    let numTeams_two = await instance.numTeams();
    assert.equal(numTeams_one, 1, "creating one team failed");
    assert.equal(numTeams_two, 2, "creating two teams failed");
  })

  it("create two teams and bet on them", async () => {
    let instance = await PredictEthSF.new();
    await instance.newTeam("zero");
    await instance.newTeam("one");
    await instance.bet(0, {from: accountZero, value: 1000000000000000})
    await instance.bet(1, {from: accountOne, value: 5000000000000000})
    let totalForZero = await instance.TeamTotalBet(0);
    let totalForOne = await instance.TeamTotalBet(1);
    assert.equal(totalForZero, 1000000000000000, "total bet for zero is wrong");
    assert.equal(totalForOne, 5000000000000000, "total bet for one is wrong");
  })

  it("create three teams and bet on two of them", async () => {
    let instance = await PredictEthSF.new();
    await instance.newTeam("zero");
    await instance.newTeam("one");
    await instance.newTeam("two");
    await instance.bet(0, {from: accountZero, value: 1000000000000000})
    await instance.bet(1, {from: accountOne, value: 5000000000000000})
    let totalForZero = await instance.TeamTotalBet(0);
    let totalForOne = await instance.TeamTotalBet(1);
    let totalForTwo = await instance.TeamTotalBet(2);
    assert.equal(totalForZero, 1000000000000000, "total bet for zero is wrong");
    assert.equal(totalForOne, 5000000000000000, "total bet for one is wrong");
    assert.equal(totalForTwo, 0, "total bet for two is wrong");
  })

  it("create two teams and bet on them, and payout", async () => {
    let instance = await PredictEthSF.new({from: accountFour});
    let initalForZero = await web3.eth.getBalance(accountZero);
    let initalForOne = await web3.eth.getBalance(accountOne);
    await instance.newTeam("zero", {from: accountThree});
    await instance.newTeam("one", {from: accountFour});
    await instance.bet(0, {from: accountZero, value: 1000000000000000000})
    await instance.bet(1, {from: accountOne, value: 5000000000000000000})
    await instance.distributePrizes([0], {from: accountFour});
    let finalForZero = await web3.eth.getBalance(accountZero);
    let finalForOne = await web3.eth.getBalance(accountOne);
    assert(Number(initalForZero) < Number(finalForZero), "zero did not receive its winnings");
    assert(Number(initalForOne) > Number(finalForOne), "one did not lose its money");
  })

  it("create four teams and bet on them, and payout", async () => {
    let instance = await PredictEthSF.new({from: accountZero});
    let initalForOne = await web3.eth.getBalance(accountOne);
    let initalForTwo = await web3.eth.getBalance(accountTwo);
    let initalForThree = await web3.eth.getBalance(accountThree);
    let initalForFour = await web3.eth.getBalance(accountFour);
    await instance.newTeam("five", {from: accountFive});
    await instance.newTeam("six", {from: accountSix});
    await instance.newTeam("seven", {from: accountSeven});
    await instance.bet(0, {from: accountOne, value: 5000000000000000000})
    await instance.bet(1, {from: accountTwo, value: 1000000000000000000})
    await instance.bet(2, {from: accountThree, value: 1000000000000000000})
    await instance.bet(2, {from: accountFour, value: 1000000000000000000})
    await instance.distributePrizes([0, 1], {from: accountZero});
    let finalForOne = await web3.eth.getBalance(accountOne);
    let finalForTwo = await web3.eth.getBalance(accountTwo);
    let finalForThree = await web3.eth.getBalance(accountThree);
    let finalForFour = await web3.eth.getBalance(accountFour);
    assert(Number(initalForOne) < Number(finalForOne), "one did not receive its winnings");
    assert(Number(initalForTwo) < Number(finalForTwo), "two did not receive its winnings");
    assert(Number(finalForOne) < Number(finalForTwo), "two did not win less than one");
    assert(Number(initalForThree) > Number(finalForThree), "three did not lose its money");
    assert(Number(initalForFour) > Number(finalForFour), "four did not lose its money");
  })

  it("create a team and change its address", async () => {
    let instance = await PredictEthSF.new({from: accountZero});
    await instance.newTeam("one", {from: accountOne});
    await instance.changeTeamAddress(0, accountTwo, {from: accountOne});
    let teamCreatorAfter = await instance.TeamCreator(0);
    assert(teamCreatorAfter == accountTwo);
  })
})
