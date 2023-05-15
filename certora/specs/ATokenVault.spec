import "methods_base.spec"


methods{
    _accrueYield() envfree => accrueYieldSummary()
}
// Rule to check the _accrueYield function
// 1. _s.lastUpdated should be equal to block.timestamp at the end
// 2. _s.accumulatedFees can only monotonically increase

// STATUS: Verified
rule accrueYieldCheck(env e){
    uint128 _accumulatedFees = getAccumulatedFees();
    uint256 _lastUpdated = getLastUpdated();
    require _lastUpdated + e.block.timestamp <= 0xffffffffff;
    
    accrueYield(e);
    
    uint256 lastUpdated_ = getLastUpdated();
    uint128 accumulatedFees_ = getAccumulatedFees();
    
    assert lastUpdated_ == e.block.timestamp,"lastUpdated should be equal to timestamp";
    assert _accumulatedFees <= accumulatedFees_,"accumulated fee can only increase or stay the same";
}


// STATUS: Verified
// rule to check that accrueYield function is called everytime some function causes a change 
// in the contract balances. This is crucial for correct accrual of fee.
rule changeInContractBalanceShouldCauseAccrual(env e, method f)
filtered { f -> !harnessOnlyMethods(f) && !f.isView }
{
    uint256 _contractATokenBal = _AToken.balanceOf(currentContract);
    uint256 _contractULBal = Underlying.balanceOf(currentContract);
    // uint256 _lastUpdated = getLastUpdated();
    // require _lastUpdated + e.block.timestamp <= 0xffffffffff;
    
    calldataarg args;
    f(e, args);

    // uint256 lastUpdated_ = getLastUpdated();
    // uint256 lastVaultBalance_ = getLastVaultBalance();
    uint256 contractATokenBal_ = _AToken.balanceOf(currentContract);
    uint256 contractULBal_ = Underlying.balanceOf(currentContract);
    assert (contractATokenBal_ != _contractATokenBal || _contractULBal != contractULBal_) && 
            (f.selector != withdrawFees(address, uint256).selector || 
            f.selector != emergencyRescue(address, address, uint256).selector) => 
            accrueYieldCalled == true,
            "contract balance change should trigger yield accrual";
}

