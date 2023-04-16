import "methods_base.spec"

// *********** RULES *************** //

// Solvency check
// STATUS: PENDING
invariant totalAssetsGESumOfBalances(env e)
    sumAllBalance() <= totalAssets(e)


// STATUS: PENDING
rule changeInContractBalanceShouldCauseAccrual(env e, method f){
    uint256 _contractATokenBal = _AToken.balanceOf(currentContract);
    uint256 _contractULBal = Underlying.balanceOf(currentContract);
    uint256 _lastUpdated = getLastUpdated();
    require _lastUpdated + e.block.timestamp <= 0xffffffffff;
    
    calldataarg args;
    f(e, args);

    uint256 lastUpdated_ = getLastUpdated();
    uint128 lastVaultBalance_ = getLastVaultBalance();
    uint256 contractATokenBal_ = _AToken.balanceOf(currentContract);
    uint256 contractULBal_ = Underlying.balanceOf(currentContract);
    assert (contractATokenBal_ != _contractATokenBal || _contractULBal != contractULBal_) => 
            lastVaultBalance_ == _contractATokenBal,
            "contract balance change should trigger yield accrual and therefore update the lastVaultBalance to the AToken balance of the contract before the Atoken balance changes ";
}

// accumulated fee should be less than contract reserves
// STATUS: PENDING
invariant accumulatedFeeLeTotalFee()
    getAccumulatedFees <= _AToken.balanceOf(currentContract)


// rule whoChangedLastUpdated(method f, env e)
// filtered{f -> !f.isView}
// {

//     uint256 _lastUpdated = getLastUpdated();
//     calldataarg args;
    
//     f(e, args);
    
//     uint256 lastUpdated_ = getLastUpdated();
//     assert lastUpdated_ == _lastUpdated;

// }



