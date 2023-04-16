import "erc20.spec"

using AToken as _AToken
using DummyERC20_aTokenUnderlying as Underlying
using SymbolicLendingPoolL1 as _SymbolicLendingPoolL1

methods{
    deposit(uint256, address) returns (uint256)
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