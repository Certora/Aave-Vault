import "erc20.spec";

using AToken as _AToken;
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1;

methods{
    function totalSupply() returns uint256 envfree;
    function balanceOf(address) returns (uint256) envfree;

    function _AToken.totalSupply() returns uint256 envfree;
    function _AToken.balanceOf(address) returns (uint256) envfree;
    function _AToken.scaledTotalSupply() returns (uint256) envfree;
    function _AToken.scaledBalanceOf(address) returns (uint256) envfree;
    function _AToken.transferFrom(address,address,uint256) returns (bool);


    //*********************  AToken.sol ********************************
    // The following was copied from StaticATokenLM spec file
    //*****************************************************************
    function mint(address,address,uint256,uint256) returns (bool) => DISPATCHER(true);
    function burn(address,address,uint256,uint256) returns (bool) => DISPATCHER(true);
    function getIncentivesController() returns (address) => CONSTANT;
    function UNDERLYING_ASSET_ADDRESS() returns (address) => CONSTANT;


    // called by AToken.sol::224. A method of IPool.
    function finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET;

    // called from: IncentivizedERC20.sol::207. A method of incentivesControllerLocal.
    function handleAction(address user, uint256 totalSupply, uint256 userBalance) => NONDET;


    // getPool() returns address => ALWAYS(100);
    function getPool() returns address => NONDET;
    
    // nissan Remark: not sure about the following 3 summarizations:

    // A method of Ipool
<<<<<<< Updated upstream
    getReserveData(address) => NONDET;
    //    _SymbolicLendingPoolL1.getReserveData(address) => NONDET;
    
    claimAllRewards(address[],address) => NONDET;

    // called in MetaTxHelpers.sol::27.
    isValidSignature(bytes32, bytes) => NONDET;
}


function mulDiv_CVL(uint256 x, uint256 y, uint256 denominator) returns uint256 {
    return to_uint256((x * y) / denominator);
}


function rayMul_CVL(uint256 a,uint256 b) returns uint256 {
    uint256 tmp = a + (a >> 2);
    return tmp;
}
function rayDiv_CVL(uint256 a,uint256 b) returns uint256 {
    uint256 tmp = a - (a >> 2);
    return tmp;
}


function maxUint128() returns uint128 {
    return 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
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



=======
    function getReserveData(address) => NONDET;
    //    _SymbolicLendingPoolL1.getReserveData(address) => NONDET;
    
    function claimAllRewards(address[],address) => NONDET;

    // called in MetaTxHelpers.sol::27.
    function isValidSignature(bytes32, bytes) => NONDET;
}

>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    preserved with (env e) {
=======
    preserved {
>>>>>>> Stashed changes
        requireInvariant sumAllBalance_eq_totalSupply();
    }
}

<<<<<<< Updated upstream
invariant lastVaultBalance_OK()
    getLastVaultBalance() == _AToken.balanceOf(currentContract)
    {
        preserved deposit(uint256 assets, address receiver) with (env e) {
            require _AToken.balanceOf(currentContract) <= maxUint128();
        }
    }

invariant lastVaultBalance_OK_2()
    _AToken.balanceOf(currentContract) <= maxUint128() =>
           getLastVaultBalance() == _AToken.balanceOf(currentContract)


/*
invariant accumulated_fee_old(env e)
    (_AToken.balanceOf(currentContract)!=0 => _AToken.balanceOf(currentContract)>getClaimableFees(e))
    &&
    (_AToken.balanceOf(currentContract)==0 => getClaimableFees(e)==0)
    {
        preserved {
            requireInvariant sumAllBalance_eq_totalSupply();
            require getLastVaultBalance() == _AToken.balanceOf(currentContract);
        }
    }
*/

invariant accumulated_fee_better(env e)
    (_AToken.balanceOf(currentContract) <= maxUint128()) =>
    (
     (_AToken.balanceOf(currentContract)!=0 => _AToken.balanceOf(currentContract)>getClaimableFees(e))
     &&
     (_AToken.balanceOf(currentContract)==0 => getClaimableFees(e)==0)
    )
    {
        preserved {
            requireInvariant sumAllBalance_eq_totalSupply();
            requireInvariant lastVaultBalance_OK_2();
        }
    }




/// If there is a non-zero share amount in the vault then the assets balance of the vault should be non-zero.
invariant inv_nonZero_shares_imply_nonZero_assets()
    totalSupply()>0 => totalAssets()>0 
//    filtered {f -> f.selector == withdraw(uint256,address,address).selector  }
    {
        preserved with (env e) {
            requireInvariant sumAllBalance_eq_totalSupply();
            requireInvariant accumulated_fee_better(e);
            requireInvariant lastVaultBalance_OK_2();
            require e.msg.sender != _AToken;

            
            //require e.msg.sender != _SymbolicLendingPoolL1;
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





=======
>>>>>>> Stashed changes

ghost sumAllATokenScaledBalance() returns mathint {
    init_state axiom sumAllATokenScaledBalance() == 0;
}

hook Sstore _AToken._userState[KEY address a] .(offset 0) uint128 balance (uint128 old_balance) STORAGE {
  havoc sumAllATokenScaledBalance assuming sumAllATokenScaledBalance@new() == sumAllATokenScaledBalance@old() + balance - old_balance;
}

hook Sload uint128 balance _AToken._userState[KEY address a] .(offset 0) STORAGE {
    require balance <= sumAllATokenScaledBalance();
<<<<<<< Updated upstream
}
=======
} 
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
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

function must_NOT_revert(method f) returns bool {
    return 
        f.selector == asset().selector ||
        f.selector == totalAssets().selector ||
        f.selector == maxDeposit(address).selector ||
        f.selector == maxMint(address).selector ||
        f.selector == maxWithdraw(address).selector ||
        f.selector == maxRedeem(address).selector
    ;
}


function must_NOT_revert_unless_large_input(method f) returns bool {
    return
        f.selector == convertToShares(uint256).selector ||
        f.selector == convertToAssets(uint256).selector
        ;
}

rule must_not_revert(method f) {
    env e;
    calldataarg args;

    require must_NOT_revert(f);
    require e.msg.value == 0;

    f@withrevert(e, args); 
    bool reverted = lastReverted;

    assert !reverted, "Conversion to assets reverted";
}





/**
 * @title ConvertToShares must not revert except for overflow
 * From EIP4626:
 * > MUST NOT revert unless due to integer overflow caused by an unreasonably large input.
 * We define large input as `10^50`. To be precise, we need that `RAY * assets < 2^256`, since
 * `2^256~=10^77` and `RAY=10^27` we get that `assets < 10^50`.
 * 
 * Note. *We also require that:* **`rate > 0`**.
 */
/*
rule toSharesDoesNotRevert(uint256 assets) {
	require assets < 10^50;
	env e;

	// Prevent revert due to overflow.
	// Roughly speaking ConvertToShares returns assets * RAY / rate().
	mathint ray_math = to_mathint(RAY());
	mathint rate_math = to_mathint(rate(e));
	mathint assets_math = to_mathint(assets);
	require rate_math > 0;

	uint256 shares = convertToShares@withrevert(e, assets);
	bool reverted = lastReverted;

	assert !reverted, "Conversion to shares reverted";
}
*/

/**
 * @title ConvertToAssets must not revert unless due to integer overflow
 * From EIP4626:
 * > MUST NOT revert unless due to integer overflow caused by an unreasonably large input.
 * We define large input as 10^45. To be precise we need that `shares * rate < 2^256 ~= 10^77`,
 * hence we require that:
 * - `shares < 10^45`
 * - `rate < 10^32`
 */
/*
rule toAssetsDoesNotRevert(uint256 shares) {
	require shares < 10^45;
	env e;

	// Prevent revert due to overflow.
	// Roughly speaking ConvertToAssets returns shares * rate() / RAY.
	mathint ray_math = to_mathint(RAY());
	mathint rate_math = to_mathint(rate(e));
	mathint shares_math = to_mathint(shares);
	require rate_math < 10^32;

	uint256 assets = convertToAssets@withrevert(e, shares);
	bool reverted = lastReverted;

	assert !reverted, "Conversion to assets reverted";
}
*/


rule previewDepositAmountCheck(){
    env e1;
    env e2;
    uint256 assets;
    address receiver;   
    uint256 previewShares;
    uint256 shares;
    
    previewShares = previewDeposit(e1, assets);
    shares = deposit(e2, assets, receiver);
    
    assert previewShares == shares,"preview shares should be equal to actual shares";
}
=======
    

>>>>>>> Stashed changes
