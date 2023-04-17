import "erc20.spec"

using AToken as _AToken
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1
using DummyERC20_aTokenUnderlying as _DummyERC20_aTokenUnderlying



methods{
    totalSupply() returns uint256 envfree;
    balanceOf(address) returns (uint256) envfree;
    totalAssets() returns (uint256) envfree;
        
    _AToken.totalSupply() returns uint256 envfree;
    _AToken.balanceOf(address) returns (uint256) envfree;
    _AToken.scaledTotalSupply() returns (uint256) envfree;
    _AToken.scaledBalanceOf(address) returns (uint256) envfree;
    _AToken.transferFrom(address,address,uint256) returns (bool);


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


    // getPool() returns address => ALWAYS(100);
    getPool() returns address => NONDET;
    
    // nissan Remark: not sure about the following 3 summarizations:

    // A method of Ipool
    getReserveData(address) => NONDET;
    //    _SymbolicLendingPoolL1.getReserveData(address) => NONDET;
    
    claimAllRewards(address[],address) => NONDET;

    // called in MetaTxHelpers.sol::27.
    isValidSignature(bytes32, bytes) => NONDET;
}


function setup(env e, address user)
{
    require currentContract != e.msg.sender;
    // require _AToken != e.msg.sender;
    // require _RewardsController != e.msg.sender;
    // require _DummyERC20_aTokenUnderlying  != e.msg.sender;
    // require _DummyERC20_rewardToken != e.msg.sender;
    // require _SymbolicLendingPoolL1 != e.msg.sender;
    // require _TransferStrategy != e.msg.sender;
    // require _ScaledBalanceToken != e.msg.sender;
    

    require currentContract != user;
    require _AToken != user;
    //    require _RewardsController !=  user;
    require _DummyERC20_aTokenUnderlying  != user;
    require _SymbolicLendingPoolL1 != user;
}



/// @title Sum of balances of StaticATokenLM 
ghost sumAllBalance() returns mathint {
    init_state axiom sumAllBalance() == 0;
}

hook Sstore _balances[KEY address a] uint256 balance (uint256 old_balance) STORAGE {
  havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
}

hook Sload uint256 balance _balances[KEY address a] STORAGE {
    require balance <= sumAllBalance();
}


invariant sumAllBalance_eq_totalSupply()
    sumAllBalance() == totalSupply()
    filtered {f -> !f.isView && f.selector != initialize(address,uint256,string,string,uint256).selector}
//  filtered {f -> f.selector == mint(uint256,address).selector} 


/// @title Static AToeknLM balancerOf(user) <= totalSupply()
invariant inv_balanceOf_leq_totalSupply(address user)
    balanceOf(user) <= totalSupply()
{
    preserved with (env e) {
        requireInvariant sumAllBalance_eq_totalSupply();
    }
}


invariant accumulated_fee(env e)
    (_AToken.balanceOf(currentContract)!=0 => _AToken.balanceOf(currentContract)>getClaimableFees(e))
    &&
    (_AToken.balanceOf(currentContract)==0 => getClaimableFees(e)==0)
    {
        preserved {
            requireInvariant sumAllBalance_eq_totalSupply();
        }
    }


/// If there is a non-zero share amount in the vault then the assets balance of the vault should be non-zero.
invariant inv_nonZero_shares_imply_nonZero_assets()
    totalSupply()>0 => totalAssets()>0 
//    filtered {f -> f.selector == withdraw(uint256,address,address).selector  }
    {
        preserved with (env e) {
            requireInvariant sumAllBalance_eq_totalSupply();
            requireInvariant accumulated_fee(e);
            require e.msg.sender != _AToken;
            //            require e.msg.sender != _SymbolicLendingPoolL1;
            //require e.msg.sender != _DummyERC20_aTokenUnderlying;        
        }
    }




/**
 * @title User AToken balance is fixed
 * Interaction with `StaticAtokenLM` should not change a user's AToken balance,
 * except for the following methods:
 * - `withdraw`
 * - `deposit`
 * - `redeem`
 * - `mint`
 * - `metaDeposit`
 * - `metaWithdraw`
 *
 * Note. Rewards methods are special cases handled in other rules below.
 *
 * Rules passed (with rule sanity): job-id=`5fdaf5eeaca249e584c2eef1d66d73c7`
 *
 * Note. `UNDERLYING_ASSET_ADDRESS()` was unresolved!
 */

/*
rule aTokenBalanceIsFixed(method f) {
	require _AToken == asset();
	require _AToken.UNDERLYING_ASSET_ADDRESS() == _DummyERC20_aTokenUnderlying;
	
	// Limit f values
	require (
		(f.selector != deposit(uint256,address).selector) &&
		(f.selector != deposit(uint256,address,uint16,bool).selector) &&
		(f.selector != withdraw(uint256,address,address).selector) &&
		(f.selector != redeem(uint256,address,address).selector) &&
		(f.selector != redeem(uint256,address,address,bool).selector) &&
		(f.selector != mint(uint256,address).selector) &&
		(f.selector != metaDeposit(
			address,address,uint256,uint16,bool,uint256,
			(address,address,uint256,uint256,uint8,bytes32,bytes32),
			(uint8, bytes32, bytes32)
		).selector) &&
		(f.selector != metaWithdraw(
			address,address,uint256,uint256,bool,uint256,
			(uint8, bytes32, bytes32)
		).selector)
	);

	// Exclude reward related methods
	require (
		(f.selector != collectAndUpdateRewards(address).selector) &&
		(f.selector != claimRewardsOnBehalf(address,address,address[]).selector) &&
		(f.selector != claimSingleRewardOnBehalf(address,address,address).selector) &&
		(f.selector != claimRewardsToSelf(address[]).selector) &&
		(f.selector != claimRewards(address,address[]).selector)
	);

	env e;

	// Limit sender
	require e.msg.sender != currentContract;
	require e.msg.sender != _AToken;

	uint256 preBalance = _AToken.balanceOf(e.msg.sender);

	calldataarg args;
	f(e, args);

	uint256 postBalance = _AToken.balanceOf(e.msg.sender);
	assert preBalance == postBalance, "aToken balance changed by static interaction";
}
*/











/*






ghost sumAllATokenScaledBalance() returns mathint {
    init_state axiom sumAllATokenScaledBalance() == 0;
}

hook Sstore _AToken._userState[KEY address a] .(offset 0) uint128 balance (uint128 old_balance) STORAGE {
  havoc sumAllATokenScaledBalance assuming sumAllATokenScaledBalance@new() == sumAllATokenScaledBalance@old() + balance - old_balance;
}

hook Sload uint128 balance _AToken._userState[KEY address a] .(offset 0) STORAGE {
    require balance <= sumAllATokenScaledBalance();
}

/// @title Sum of AToken scaled balances = AToken scaled totalSupply()
invariant sumAllATokenScaledBalance_eq_totalSupply()
    sumAllATokenScaledBalance() == _AToken.scaledTotalSupply()


/// @title AToken scaledBalancerOf(user) <= AToken.scaledTotalSupply()
invariant inv_atoken_scaled_balanceOf_leq_totalSupply(address user)
    _AToken.scaledBalanceOf(user) <= _AToken.scaledTotalSupply()
    {
        preserved {
            requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
        }
    }

/// @title AToken sum of 2 balancers <= AToken totalSupply()
invariant inv_atoken_balanceOf_2users_leq_totalSupply(address user1, address user2)
    (_AToken.balanceOf(user1) + _AToken.balanceOf(user2))<= _AToken.totalSupply()
{
    preserved with (env e1){
        setup(e1, user1);
        setup(e1, user2);
    }
    preserved redeem(uint256 shares, address receiver, address owner) with (env e2){
        require user1 != user2;
        require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
    }
    preserved redeem(uint256 shares, address receiver, address owner, bool toUnderlying) with (env e3){
        require user1 != user2;
        requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
        require _AToken.balanceOf(e3.msg.sender) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
        require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
    }
    preserved withdraw(uint256 assets, address receiver,address owner) with (env e4){
        require user1 != user2;
        requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
        require _AToken.balanceOf(e4.msg.sender) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
        require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
    }
    
    preserved metaWithdraw(address owner, address recipient,uint256 staticAmount,uint256 dynamicAmount,bool toUnderlying,uint256 deadline,_StaticATokenLM.SignatureParams sigParams)
        with (env e5){
        require user1 != user2;
        requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
        require _AToken.balanceOf(e5.msg.sender) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
        require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
    }    
}

    

*/




rule larger_deposit_imply_more_shares() {
    address receiver;
    uint256 assets;

    require(assets > 100);

    uint256 balance_receiver_pre = _AToken.balanceOf(receiver);

    env e;
    deposit(e,assets,receiver);
    
    uint256 balance_receiver_after = _AToken.balanceOf(receiver);

    assert (balance_receiver_after >= balance_receiver_pre+1000);
}
