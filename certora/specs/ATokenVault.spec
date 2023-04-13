import "erc20.spec"

using AToken as _AToken
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1

methods{
    
    getLastUpdated() returns (uint256) envfree
    accrueYield()
    // _accrueYield() => ay()
    totalSupply() returns uint256 envfree
    balanceOf(address) returns (uint256) envfree

    _AToken.totalSupply() returns uint256 envfree
    _AToken.balanceOf(address) returns (uint256) envfree
    _AToken.scaledTotalSupply() returns (uint256) envfree
    _AToken.scaledBalanceOf(address) returns (uint256) envfree
    _AToken.transferFrom(address,address,uint256) returns (bool)


    // //*********************  AToken.sol ********************************
    // // The following was copied from StaticATokenLM spec file
    // //*****************************************************************
    mint(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    burn(address,address,uint256,uint256) returns (bool) => DISPATCHER(true)
    getIncentivesController() returns (address) => CONSTANT
    UNDERLYING_ASSET_ADDRESS() returns (address) => CONSTANT


    // called by AToken.sol::224. A method of IPool.
    finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET

    // called from: IncentivizedERC20.sol::207. A method of incentivesControllerLocal.
    handleAction(address,uint256,uint256) => DISPATCHER(true)

    // getPool() returns address => ALWAYS(100);
    getPool() returns address => NONDET;
    
    // // nissan Remark: not sure about the following 3 summarizations:

    // A method of Ipool
    // can this contract change the pool
    getReserveData(address) => CONSTANT;
    
    claimAllRewards(address[],address) => NONDET;

    // called in MetaTxHelpers.sol::27.
    isValidSignature(bytes32, bytes) => NONDET;
}


ghost sumAllBalance() returns mathint {
    init_state axiom sumAllBalance() == 0;
}

hook Sstore _balances[KEY address a] uint256 balance (uint256 old_balance) STORAGE {
  havoc sumAllBalance assuming sumAllBalance@new() == sumAllBalance@old() + balance - old_balance;
}

hook Sload uint256 balance _balances[KEY address a] STORAGE {
    require balance <= sumAllBalance();
}

// *********** CVL functions ************* //

// Empty CVL function to bypass the _accrueYield function
function ay(){
    uint40 sum = 1;
}

// *********** RULES *************** //
// view function filter
rule changeInContractBalanceShouldCauseAccrual(env e, method f){
    uint256 _contractATokenBal = _AToken.balanceOf(currentContract);
    uint256 _lastUpdated = getLastUpdated();
    require _lastUpdated + e.block.timestamp <= 0xffffffffff;
    
    calldataarg args;
    f(e, args);

    uint256 lastUpdated_ = getLastUpdated();
    uint256 contractATokenBal_ = _AToken.balanceOf(currentContract);
    assert contractATokenBal_ != _contractATokenBal => lastUpdated_ == e.block.timestamp,"contract balance change should trigger yield accrual and hence update lastUpdated";
}


// Checking that only _accrueYield function can change lastUpdated. rule run with the _accrueYield function summarized as an empty CVL function. 
rule lastUpdatedDoesntChange(env e, method f){
    uint256 _lastUpdated = getLastUpdated();
    
    calldataarg args;
    f(e, args);

    uint256 lastUpdated_ = getLastUpdated();

    assert lastUpdated_ == _lastUpdated,"last updated should not change";
}
// overflow when downcasting to uint40 can lead to wrong update of lastUpdated
// STATUS: Verified
// https://prover.certora.com/output/11775/9613d6eb286849aca053afa96562c566/?anonymousKey=a3373d815cdd9b37b5f719ac08a804dadacc2b3c
rule accrueYieldUpdatesLastUpdated(env e){
    uint256 _lastUpdated = getLastUpdated();
    // to avoid overflow in downcasting to uint40
    require e.block.timestamp <= 0xffffffffff;

    accrueYield(e);

    uint256 lastUpdated_ = getLastUpdated();
    assert lastUpdated_ == e.block.timestamp,"accrueYield should update the lastUpdated value to current timestamp";
}



invariant totalAssetsGESumOfBalances(env e)
    sumAllBalance() <= totalAssets(e)

// invariant sumAllBalance_eq_totalSupply()
//     sumAllBalance() == totalSupply()
    // filtered {f -> !f.isView && f.selector != initialize(address,uint256,string,string,uint256).selector}
//  filtered {f -> f.selector == mint(uint256,address).selector} 


// /// @title Static AToeknLM balancerOf(user) <= totalSupply()
// invariant inv_balanceOf_leq_totalSupply(address user)
//     balanceOf(user) <= totalSupply()
// {
//     preserved {
//         requireInvariant sumAllBalance_eq_totalSupply();
//     }
// }


// ghost sumAllATokenScaledBalance() returns mathint {
//     init_state axiom sumAllATokenScaledBalance() == 0;
// }

// hook Sstore _AToken._userState[KEY address a] .(offset 0) uint128 balance (uint128 old_balance) STORAGE {
//   havoc sumAllATokenScaledBalance assuming sumAllATokenScaledBalance@new() == sumAllATokenScaledBalance@old() + balance - old_balance;
// }

// hook Sload uint128 balance _AToken._userState[KEY address a] .(offset 0) STORAGE {
//     require balance <= sumAllATokenScaledBalance();
// } 

// /// @title Sum of AToken scaled balances = AToken scaled totalSupply()
// invariant sumAllATokenScaledBalance_eq_totalSupply()
//     sumAllATokenScaledBalance() == _AToken.scaledTotalSupply()


// /// @title AToken scaledBalancerOf(user) <= AToken.scaledTotalSupply()
// invariant inv_atoken_scaled_balanceOf_leq_totalSupply(address user)
//     _AToken.scaledBalanceOf(user) <= _AToken.scaledTotalSupply()
//     {
//         preserved {
//             requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
//         }
//     }

// /// @title AToken sum of 2 balancers <= AToken totalSupply()
// invariant inv_atoken_balanceOf_2users_leq_totalSupply(address user1, address user2)
//     (_AToken.balanceOf(user1) + _AToken.balanceOf(user2))<= _AToken.totalSupply()
// {
//     preserved with (env e1){
//         setup(e1, user1);
//         setup(e1, user2);
//     }
//     preserved redeem(uint256 shares, address receiver, address owner) with (env e2){
//         require user1 != user2;
//         require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
//     }
//     preserved redeem(uint256 shares, address receiver, address owner, bool toUnderlying) with (env e3){
//         require user1 != user2;
//         requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
//         require _AToken.balanceOf(e3.msg.sender) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
//         require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
//     }
//     preserved withdraw(uint256 assets, address receiver,address owner) with (env e4){
//         require user1 != user2;
//         requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
//         require _AToken.balanceOf(e4.msg.sender) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
//         require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
//     }
    
//     preserved metaWithdraw(address owner, address recipient,uint256 staticAmount,uint256 dynamicAmount,bool toUnderlying,uint256 deadline,_StaticATokenLM.SignatureParams sigParams)
//         with (env e5){
//         require user1 != user2;
//         requireInvariant sumAllATokenScaledBalance_eq_totalSupply();
//         require _AToken.balanceOf(e5.msg.sender) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
//         require _AToken.balanceOf(currentContract) + _AToken.balanceOf(user1) + _AToken.balanceOf(user2) <= _AToken.totalSupply();
//     }    
// }

    

