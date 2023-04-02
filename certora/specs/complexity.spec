import "erc20.spec"

methods{
    //*********************  AToken.sol ********************************
    // The following was copied from StaticATokenLM spec file
    //*****************************************************************
    mint(address,address,uint256,uint256) returns (bool) => DISPATCHER(true);
    burn(address,address,uint256,uint256) returns (bool) => DISPATCHER(true);
    getIncentivesController() returns (address) => CONSTANT;
    UNDERLYING_ASSET_ADDRESS() returns (address) => CONSTANT;


    // called by AToken.sol::224. A method of IPool.
    finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET;

    // called from: IncentivizedERC20.sol::207. A method of incentivesControllerLocal.
    handleAction(address user, uint256 totalSupply, uint256 userBalance) => NONDET;



    // nissan Remark: not sure about the following 3 summarizations:

    // A method of Ipool
    getReserveData(address) => NONDET;
    

    // called in MetaTxHelpers.sol::27.
    isValidSignature(bytes32, bytes) => NONDET;

    // For some reason the following 2 summarizations are ignored in the constractor
    getPool() returns address => NONDET;
    claimAllRewards(address[],address) => NONDET;
}




rule sanity(method f)
{
	env e;
	calldataarg args;
	f(e,args);
	assert false, "REACHED FALSE !";
}


/*
This rule find which functions never reverts.

*/


rule noRevert(method f)
description "$f has reverting paths"
{
	env e;
	calldataarg arg;
	require e.msg.value == 0;
	f@withrevert(e, arg);
	assert !lastReverted, "${f.selector} can revert";
}


rule alwaysRevert(method f)
description "$f has reverting paths"
{
	env e;
	calldataarg arg;
	f@withrevert(e, arg); 
	assert lastReverted, "${f.selector} succeeds";
}


/*
This rule find which functions that can be called, may fail due to someone else calling a function right before.

This is n expensive rule - might fail on the demo site on big contracts
*/

rule simpleFrontRunning(method f, address privileged) filtered { f-> !f.isView }
description "$f can no longer be called after it had been called by someone else"
{
	env e1;
	calldataarg arg;
    
	storage initialStorage = lastStorage;
	f(e1, arg);

	env e2;
	calldataarg arg2;
	require e2.msg.sender != e1.msg.sender;
	f(e2, arg2) at initialStorage;
	f@withrevert(e1, arg);
	bool succeeded = !lastReverted;

	assert succeeded, "${f.selector} can be not be called if was called by someone else";
}


/*
This rule find which functions are privileged.
A function is privileged if there is only one address that can call it.

The rules finds this by finding which functions can be called by two different users.

*/


rule privilegedOperation(method f, address privileged)
description "$f can be called by more than one user without reverting"
{
	env e1;
	calldataarg arg;
	require e1.msg.sender == privileged;

	storage initialStorage = lastStorage;
	f@withrevert(e1, arg); // privileged succeeds executing candidate privileged operation.
	bool firstSucceeded = !lastReverted;

	env e2;
	calldataarg arg2;
	require e2.msg.sender != privileged;
	f@withrevert(e2, arg2) at initialStorage; // unprivileged
	bool secondSucceeded = !lastReverted;

	assert  !(firstSucceeded && secondSucceeded), "${f.selector} can be called by both ${e1.msg.sender} and ${e2.msg.sender}, so it is not privileged";
}

rule whoChangedBalanceOf(method f, address u) {
    env eB;
    env eF;
    calldataarg args;
    uint256 before = balanceOf(eB, u);
    f(eF,args);
    assert balanceOf(eB, u) == before, "balanceOf changed";
}
