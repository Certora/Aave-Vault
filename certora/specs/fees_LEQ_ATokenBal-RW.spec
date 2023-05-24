import "methods_base.spec"
using ATokenVaultHarness as _ATokenVaultHarness



methods {
    Underlying.totalSupply() envfree;
    havoc_all() envfree;
    _SymbolicLendingPoolL1.getLiquidityIndex() envfree;

    rayMul(uint256 a,uint256 b) returns (uint256) => rayMul_g(a,b);
    rayDiv(uint256 a,uint256 b) returns (uint256) => rayDiv_g(a,b);
    
    havoc_all_dummy() => HAVOC_ALL;
    mulDiv(uint256 x, uint256 y, uint256 denominator, uint8 rounding) returns uint256 =>
        mulDiv4_g(x,y,denominator,rounding);
}

ghost mulDiv4_g(uint256 , uint256 , uint256, uint8) returns uint256 {
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding.
        (
         (mulDiv4_g(x,y,denominator,rounding)*denominator <= x*y)
         &&
         (y<=denominator => mulDiv4_g(x,y,denominator,rounding)<=x)
        );
}

/*
ghost mulDiv4_g(uint256 , uint256 , uint256, uint8) returns uint256 {
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding.
        mulDiv4_g(x,y,denominator,rounding)*denominator <= x*y;
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding. 
        y<=denominator => mulDiv4_g(x,y,denominator,rounding)<=x;
}
*/
ghost rayMul_g(uint256 , uint256) returns uint256 {
    axiom forall uint256 x. forall uint256 y.
        (
         ((x==0||y==0) => rayMul_g(x,y)==0)
         &&
         x <= rayMul_g(x,y) && rayMul_g(x,y) <= 2*x
        );
}
ghost rayDiv_g(uint256 , uint256) returns uint256 {
    axiom forall uint256 x. forall uint256 y.
        (
         x/2 <= rayDiv_g(x,y) && rayDiv_g(x,y) <= x
        );
}



function max_possible_fees() returns uint256 {
    return to_uint256(getAccumulatedFees()
                      +
                      (_AToken.balanceOf(currentContract)-getLastVaultBalance())/2
                     );
}



// ******************************************************************************
// The following 3 invariants are proved in totalSupply_EQ_sumAllBal.spec
// ******************************************************************************
invariant inv_sumAllBalance_eq_totalSupply__underline()
    sumAllBalance_underline() == Underlying.totalSupply()

invariant inv_sumAllBalance_eq_totalSupply__atoken()
    sumAllBalance_atoken() == _AToken.scaledTotalSupply()

invariant inv_sumAllBalance_eq_totalSupply()
    sumAllBalance() == totalSupply()


// ******************************************************************************
// The following invariant is proved in lastVaultBalance_OK.spec
// ******************************************************************************
invariant lastVaultBalance_OK()
    getLastVaultBalance() <= _AToken.balanceOf(currentContract)




// ******************************************************************************
// Proving the solvency rule:
//           getClaimableFees() <= ATOKEN.balanceOf(theVault).
// We do it by proving the stronger invariant:
//           max_possible_fees() <= _AToken.balanceOf(currentContract)
// 
// In this file we prove the following methods: withraw*\redeem*\withdrawFees. (The other
// methods are treated in fee_LEQ_ATokenBal.spec.)
// Note: the reason for the seperation is that different methods require different summarizations.
//
// Status: fail! reported to Aave.
// See: https://certora.slack.com/archives/CUDKSJ41M/p1684332844321569
// ******************************************************************************
    
rule rl_getClaimableFees_LEQ_ATokenBalance(method f, env e) {
    require(f.selector != havoc_all().selector);
    require(
            f.selector == withdrawFees(address,uint256).selector ||
            f.selector == redeem(uint256,address,address).selector ||
            f.selector == redeemAsATokens(uint256,address,address).selector ||
            f.selector == withdraw(uint256,address,address).selector ||
            f.selector == withdrawATokens(uint256,address,address).selector ||

            f.selector == withdrawWithSig(uint256,address,address,
                                          (uint8,bytes32,bytes32,uint256)).selector ||
            f.selector == withdrawATokensWithSig(uint256,address,address,
                                                 (uint8,bytes32,bytes32,uint256)).selector ||

            f.selector == redeemWithSig(uint256,address,address,
                                        (uint8,bytes32,bytes32,uint256)).selector ||
            
            f.selector == redeemWithATokensWithSig(uint256,address,address,
            (uint8,bytes32,bytes32,uint256)).selector
    );

    require getLastUpdated() <= e.block.timestamp;
    require e.msg.sender != currentContract;

    //    require e1.block.timestamp <= e2.block.timestamp;
    //require e2.block.timestamp < e3.block.timestamp;
    //require e3.block.timestamp <= 0xffffff;
    
    require getFee() <= SCALE();  // SCALE is 10^18
    require _AToken.balanceOf(currentContract) <= maxUint64();
    require totalSupply() <= maxUint64();
    require Underlying.totalSupply() <= maxUint64();
    require _AToken.scaledTotalSupply() <= maxUint64();
    requireInvariant inv_sumAllBalance_eq_totalSupply__underline(); 
    requireInvariant inv_sumAllBalance_eq_totalSupply__atoken(); 
    requireInvariant inv_sumAllBalance_eq_totalSupply();
    requireInvariant lastVaultBalance_OK();
    
    uint256 ind = _SymbolicLendingPoolL1.getLiquidityIndex();
    uint256 s_bal = _AToken.scaledBalanceOf(currentContract);

    // The following require means: (s_bal - ass/ind)*ind == s_bal*ind - ass
    require (forall uint256 ass.
             rayMul_g(to_uint256(s_bal-rayDiv_g(ass,ind)),ind) == to_uint256(rayMul_g(s_bal,ind)-ass)
            );

    // The following require means: (x/ind+z)*ind == x+z*ind 
    //require (forall uint256 x. forall uint256 ind. forall uint256 z.
    //         rayMul_g(to_uint256(rayDiv_g(x,ind)+z),ind) == to_uint256(x+rayMul_g(z,ind))
    //        );
    
    require(_AToken.balanceOf(currentContract) < 1000);
    require(getAccumulatedFees()*2 <= _AToken.balanceOf(currentContract));
    require(max_possible_fees() <= _AToken.balanceOf(currentContract));

    //uint256 shares;
    //address receiver;
    //address owner;
    //redeem(e2, shares, receiver, owner);
    
    calldataarg args;
    f(e,args);


    assert(max_possible_fees() <= _AToken.balanceOf(currentContract));
}


invariant inv_fees_LEQ_lastVaultBal()
    getAccumulatedFees() <= getLastVaultBalance() {
    preserved {
        require getFee() <= SCALE();  // SCALE is 10^18
        require _AToken.balanceOf(currentContract) <= maxUint64();
        require totalSupply() <= maxUint64();
        require Underlying.totalSupply() <= maxUint64();
        require _AToken.scaledTotalSupply() <= maxUint64();
        requireInvariant inv_sumAllBalance_eq_totalSupply();
        requireInvariant inv_sumAllBalance_eq_totalSupply__atoken();
        requireInvariant inv_sumAllBalance_eq_totalSupply__underline();
        requireInvariant lastVaultBalance_OK();
        require _AToken.balanceOf(currentContract) <= 100;
    }
}
    
    
