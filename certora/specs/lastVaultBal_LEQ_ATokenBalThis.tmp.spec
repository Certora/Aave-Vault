import "methods_base.spec";

methods {
    function Underlying.totalSupply() external envfree;
    function havoc_all() external envfree;
    function _SymbolicLendingPoolL1.getLiquidityIndex() external envfree;

    //    rayMul(uint256 a,uint256 b) returns (uint256) => rayMul_g(a,b);
    //rayDiv(uint256 a,uint256 b) returns (uint256) => rayDiv_g(a,b);
    function _.mulDiv(uint256 x, uint256 y, uint256 denominator) returns uint256 => mulDiv_CVL(x,y,denominator);
    
    function _.havoc_all_dummy() => HAVOC_ALL;
}

function mulDiv_CVL(uint256 x, uint256 y, uint256 denominator) returns uint256 {
    require (denominator != 0);
    return to_uint256((x * y) / denominator);
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
// The main invariant of this file:
// _s.lastVaultBalance <= ATOKEN.balanceOf(theVault).
//
// Status: pass for all methods.
//
// Note: We require that the totalSupply of currentContract, AToken, Underlying to be
//       less than maxUint64() to avoid failures due to overflows.
// ******************************************************************************
 
invariant inv_lastVaultBalance_LEQ_ATokenBalThis()
    getLastVaultBalance() <= _AToken.balanceOf(currentContract)+1
    filtered {f ->
    f.selector != sig:initialize(address,uint256,string,string,uint256).selector &&
    f.selector != sig:havoc_all().selector
} {
    preserved with (env e) {
        require e.msg.sender != currentContract;
        require getFee() <= SCALE();  // SCALE is 10^18
        require _AToken.balanceOf(currentContract) <= maxUint64();
        require totalSupply() <= maxUint64();
        require Underlying.totalSupply() <= maxUint64();
        require _AToken.scaledTotalSupply() <= maxUint64();
        require _SymbolicLendingPoolL1.getLiquidityIndex() >= RAY();
        require _SymbolicLendingPoolL1.getLiquidityIndex() <= 2*RAY();
        requireInvariant inv_sumAllBalance_eq_totalSupply__underline(); 
        requireInvariant inv_sumAllBalance_eq_totalSupply__atoken(); 
        requireInvariant inv_sumAllBalance_eq_totalSupply();
    }
    
    preserved withdrawFees(address to, uint256 amount) with (env e) {
        require _AToken.balanceOf(currentContract) <= maxUint64();
        require totalSupply() <= maxUint64();
        require e.msg.sender != currentContract;
        require getFee() <= SCALE();  // SCALE is 10^18
        require Underlying.totalSupply() <= maxUint64();
        require _AToken.scaledTotalSupply() <= maxUint64();
        require _SymbolicLendingPoolL1.getLiquidityIndex() >= RAY();
        require _SymbolicLendingPoolL1.getLiquidityIndex() <= 2*RAY();
        requireInvariant inv_sumAllBalance_eq_totalSupply__underline(); 
        requireInvariant inv_sumAllBalance_eq_totalSupply__atoken(); 
        requireInvariant inv_sumAllBalance_eq_totalSupply();

        require to != currentContract;
    }

    preserved depositATokensWithSig(uint256 assets,address receiver,address depositor
                                    ,_ATokenVaultHarness.EIP712Signature sig
                                   ) with (env e) {
        require e.msg.sender != currentContract;
        require getFee() <= SCALE();  // SCALE is 10^18
        require _AToken.balanceOf(currentContract) <= maxUint64();
        require totalSupply() <= maxUint64();
        require Underlying.totalSupply() <= maxUint64();
        require _AToken.scaledTotalSupply() <= maxUint64();
        require _SymbolicLendingPoolL1.getLiquidityIndex() >= RAY();
        require _SymbolicLendingPoolL1.getLiquidityIndex() <= 2*RAY();
        requireInvariant inv_sumAllBalance_eq_totalSupply__underline(); 
        requireInvariant inv_sumAllBalance_eq_totalSupply__atoken(); 
        requireInvariant inv_sumAllBalance_eq_totalSupply();
        require depositor != currentContract;
    }
    
    preserved mintWithATokensWithSig(uint256 assets,address receiver,address depositor
                                     ,_ATokenVaultHarness.EIP712Signature sig
                                    ) with (env e) {
        require e.msg.sender != currentContract;
        require getFee() <= SCALE();  // SCALE is 10^18
        require _AToken.balanceOf(currentContract) <= maxUint64();
        require totalSupply() <= maxUint64();
        require Underlying.totalSupply() <= maxUint64();
        require _AToken.scaledTotalSupply() <= maxUint64();
        require _SymbolicLendingPoolL1.getLiquidityIndex() >= RAY();
        require _SymbolicLendingPoolL1.getLiquidityIndex() <= 2*RAY();
        requireInvariant inv_sumAllBalance_eq_totalSupply__underline(); 
        requireInvariant inv_sumAllBalance_eq_totalSupply__atoken(); 
        requireInvariant inv_sumAllBalance_eq_totalSupply();
        require depositor != currentContract;
    }
    
}




rule rl_lastVaultBalance_LEQ_ATokenBalThis(env e) {
    require e.msg.sender != currentContract;
    require getFee() <= SCALE();  // SCALE is 10^18
    require _AToken.balanceOf(currentContract) <= maxUint64();
    require totalSupply() <= maxUint64();
    require Underlying.totalSupply() <= maxUint64();
    require _AToken.scaledTotalSupply() <= maxUint64();
    require _SymbolicLendingPoolL1.getLiquidityIndex() >= RAY();
    require _SymbolicLendingPoolL1.getLiquidityIndex() <= 2*RAY();
    requireInvariant inv_sumAllBalance_eq_totalSupply__underline(); 
    requireInvariant inv_sumAllBalance_eq_totalSupply__atoken(); 
    requireInvariant inv_sumAllBalance_eq_totalSupply();
    
    require(getLastVaultBalance() <= _AToken.balanceOf(currentContract));
    
    
    uint256 assets;
    address receiver;
    depositATokens(e,assets,receiver);

    assert(getLastVaultBalance() <= _AToken.balanceOf(currentContract) +200);
}

