import "methods_base.spec";


methods{
    //function _.rayMul(uint256 x, uint256 y) returns (uint256) envfree => rayMul_g(x,y);
    //function _.rayDiv(uint256 x, uint256 y) returns (uint256) envfree => rayDiv_g(x,y);
    //function _.mulDiv(uint256 x, uint256 y, uint256 denominator, uint8 rounding) returns (uint256) envfree => mulDiv_g(x,y,denominator,rounding);

    function _.rayMul(uint256 a,uint256 b) internal => rayMul_g(a,b) expect uint256 ALL;
    function _.rayDiv(uint256 a,uint256 b) internal => rayDiv_g(a,b) expect uint256 ALL;
    function _.mulDiv(uint256 x, uint256 y, uint256 denominator, uint8 rounding) internal => mulDiv_g(x,y,denominator,rounding)  expect uint256 ALL;
}

ghost rayMul_g(uint256, uint256) returns uint256{
    axiom forall uint256 x. forall uint256 y. rayMul_g(x,y)*RAY()<= x*y + RAY()/2;
    axiom forall uint256 x. forall uint256 y. x*y - RAY()/2< rayMul_g(x,y)*RAY();
}

ghost rayDiv_g(uint256, uint256) returns uint256{
    axiom forall uint256 x. forall uint256 y. rayDiv_g(x,y)*y<= x*RAY() + y/2;
    axiom forall uint256 x. forall uint256 y. x*RAY() - y/2 < rayDiv_g(x,y)*y;
}

// axiom f * deno < x*y
// axioms for requirement in CVL function

ghost mulDiv_g(uint256, uint256, uint256, uint8) returns uint256 {
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding.
    rounding == 0 => mulDiv_g(x, y, denominator, rounding)*denominator <= x*y;
    
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding.
    rounding == 1 => mulDiv_g(x, y, denominator, rounding)*denominator <= x*y+denominator;
    
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding. 
    rounding == 0 => x*y < mulDiv_g(x,y,denominator, rounding)*denominator + denominator;
    
    axiom forall uint256 x. forall uint256 y. forall uint256 denominator. forall uint8 rounding.
    rounding == 1 => x*y < mulDiv_g(x,y,denominator, rounding)*denominator;
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


