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
*/

ghost rayMul_g(uint256 , uint256) returns uint256 {
    axiom forall uint256 x. forall uint256 y.rayMul_g(x,y)==x;
}
ghost rayDiv_g(uint256 , uint256) returns uint256 {
    axiom forall uint256 x. forall uint256 y. rayDiv_g(x,y)==x;
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





/*
invariant nonZeroSupplyNonZeroAssets(env e1)
    totalSupply() != 0 => totalAssets(e1) != 0
    filtered {f -> f.selector == deposit(uint256,address).selector}
// filtered {f -> f.selector == depositATokens(uint256,address).selector}
// filtered { f -> !harnessOnlyMethods(f) && !f.isView }
    {
        preserved with (env e2) {
            require e1.msg.sender == e2.msg.sender;
            require e2.msg.sender != currentContract;
            
            require _SymbolicLendingPoolL1.getLiquidityIndex() >= RAY();
            // fee set to 100% can cause unbacked shares to be minted
            require getFee() < SCALE();
        }
    }
*/

rule rl_nonZeroSupplyNonZeroAssets(method f, env e1, env e2, env e3) {
    require(f.selector != havoc_all().selector);

    require getLastUpdated() <= e1.block.timestamp;
    require e1.block.timestamp <= e2.block.timestamp;
    require e2.block.timestamp <= e3.block.timestamp;
    require e3.block.timestamp <= 0xffffff;

    require e2.msg.sender != currentContract;
    
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

    //The following require means: (x/ind+z)*ind == x+z*ind 
    require (forall uint256 x. forall uint256 ind. forall uint256 z.
             rayMul_g(to_uint256(rayDiv_g(x,ind)+z),ind) == to_uint256(x+rayMul_g(z,ind))
            );

    
    require(_AToken.balanceOf(currentContract) < 1000);
    require(totalSupply() != 0 => totalAssets(e1) != 0);
    //uint256 shares;
    //address receiver;
    //address owner;
    //redeem(e2, shares, receiver, owner);

    uint256 totS=totalSupply();
    uint256 totA=totalAssets(e2);
    
    require (forall uint256 assets. forall uint8 rnd.
             totA-assets == 0  =>  totS-mulDiv4_g(assets,totS,totA,rnd) == 0
            );

    if (f.selector == depositATokensWithSig(uint256,address,address,(uint8,bytes32,bytes32,uint256)).selector) {
        uint256 assets; address receiver; address depositor; _ATokenVaultHarness.EIP712Signature sig;
        require depositor != currentContract;
        depositATokensWithSig(e2,assets,receiver,depositor,sig);
    }
    if (f.selector == mintWithATokensWithSig(uint256,address,address,(uint8,bytes32,bytes32,uint256)).selector) {
        uint256 shares; address receiver; address depositor; _ATokenVaultHarness.EIP712Signature sig;
        require depositor != currentContract;
        mintWithATokensWithSig(e2, shares, receiver, depositor, sig);
    }
    else {
        calldataarg args;
        f(e2,args);
    }

    assert(totalSupply() != 0 => totalAssets(e3) != 0);
}
