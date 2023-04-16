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


// Rule to check that when lastUpdated changes, it can only change to the block.timestamp and the 
// If this property doesn't hold, it would mean that the 


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

// deposit flow check rule
rule depositCheck(){
    uint256 assets;
    address receiver;
    env e;
    deposit(e, assets, receiver);
    assert false;
}

rule whoChangedLastUpdated(method f, env e)
filtered{f -> !f.isView}
{

    uint256 _lastUpdated = getLastUpdated();
    calldataarg args;
    
    f(e, args);
    
    uint256 lastUpdated_ = getLastUpdated();
    assert lastUpdated_ == _lastUpdated;

}

// accumulated fee should be less than contract reserves
// STATUS: PENDING
invariant accumulatedFeeLeTotalFee()
    getAccumulatedFees <= _AToken.balanceOf(currentContract)


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

    

