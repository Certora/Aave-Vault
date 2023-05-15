import "methods_base.spec"

// *********** RULES *************** //

// non-zero total supply => non-zero assets

// ISSUES:

// 1. depositing < 1AToken amount could lead to unbacked shares being minted.
// https://prover.certora.com/output/11775/5a4b099cb31e4368a92baa0c02abcfec/?anonymousKey=b208772ac521af582729a6e3b36fbc2cdb1e40be

// 2. Fee set to 100% with starting state of zero supply and assets can lead to unbacked shares being minted. (small issue)
// https://prover.certora.com/output/11775/d82c33320e4449e0b15fd6469623a366/?anonymousKey=0d54c98a51be009ae4014cd17f69ce34440c4d49

// 3. index >= 1 to avoid violation where 1 UL is deposited but it's not reflected in the balance reading of the contract
// https://prover.certora.com/output/11775/9771b65fe08c45d891d6309b5bacac3b/?anonymousKey=ab56c70c4d8493424a70be1fc565c64128a871d8

// STATUS: PENDING
invariant nonZeroSupplyNonZeroAssets(env e1)
    totalSupply() != 0 => totalAssets(e1) != 0
    filtered {f -> f.selector == deposit(uint256,address).selector}
    // filtered {f -> f.selector == depositATokens(uint256,address).selector}
    // filtered { f -> !harnessOnlyMethods(f) && !f.isView }
    { preserved with (env e2) { require e1.msg.sender == e2.msg.sender;
                                require e2.msg.sender != currentContract;
                                
                                require _SymbolicLendingPoolL1.getReserveNormalizedIncome(e2, Underlying) >= RAY();
                                // fee set to 100% can cause unbacked shares to be minted
                                require getFee() < SCALE();} }
// index across all contracts should be the same

// rule to check solvency for deposit function
// STATUS: PENDING
rule depositcheck()
    // filtered {f -> depositWithoutSignatureMethods(f)}
    {
        uint256 assets;
        address receiver;
        env e1;
        uint256 index = _SymbolicLendingPoolL1.getReserveNormalizedIncome(e1, Underlying);
        require index == 2* RAY();
        require totalSupply() != 0 => totalAssets(e1) != 0;

        env e2;
        require e2.msg.sender != currentContract;
        deposit(e2, assets, receiver);

        assert assets*RAY()/index >= 1 => (totalSupply() != 0 => totalAssets(e1) != 0),"solvency fail";
    }

// rule to check solvency for depositAToken function
// STATUS: PENDING
rule depositATokencheck()
    // filtered {f -> depositWithoutSignatureMethods(f)}
    {
        uint256 assets;
        address receiver;
        env e1;
        uint256 index = _SymbolicLendingPoolL1.getReserveNormalizedIncome(e1, Underlying);
        require index == 2* RAY();
        require totalSupply() != 0 => totalAssets(e1) != 0;

        env e2;
        require e2.msg.sender != currentContract;
        depositATokens(e2, assets, receiver);

        assert assets*RAY()/index >= 1 => (totalSupply() != 0 => totalAssets(e1) != 0),"solvency fail";
    }



// Other solvency checks

// invariant to check that the sum of all shares is less than or equal to totalAssets.
// STATUS: PENDING
invariant totalAssetsGESumOfBalances(env e)
    sumAllBalance() <= totalAssets(e)
    filtered { f -> !harnessOnlyMethods(f) && !f.isView }

// invariant to check that the totalSupply is less than or equal to totalAssets.
invariant supplyLETotalAssets(env e)
    totalSupply() <= totalAssets(e)
    // filtered {f -> f.selector == deposit(uint256, address).selector}
    filtered { f -> !harnessOnlyMethods(f) && !f.isView }

// invariant to check that if there is a non-zero supply of shares, then there should be some assets to back those shares
// STATUS: PENDING
invariant nonZeroSharesNonZeroAssets(env e)
    sumAllBalance() != 0 => totalAssets(e) != 0
    // filtered {f -> f.selector == redeem(uint256,address,address).selector}
    filtered { f -> !harnessOnlyMethods(f) && !f.isView }
    { preserved { requireInvariant totalSupplyESumAllBalance(); } }


// invariant to prove that sumAllBalance ghost is equal to total Supply
// STATUS: PENDING
invariant totalSupplyESumAllBalance()
    totalSupply() == sumAllBalance()
    filtered { f -> !harnessOnlyMethods(f) && !f.isView }
// invariant to prove that the totalSupply should be greater than or equal to the shares held by any one user.
// STATUS: PENDING
invariant totalSupplyGeUserBalance(address user)
    totalSupply() >= balanceOf(user)
    filtered { f -> !harnessOnlyMethods(f) && !f.isView }


// Redemption front-running: A user with a given number of shares should be able to redeem them for the same amount of assets
// regardless of actions by another user. The pupose of this rule is to check that the conversion ratio of shares into assets
// is not impacted by actions of another user

// requiring that totalSupply !=0 after the parametric call in order to avoid cases where returned asset amount is 
// equal to specified share amount

// using previewRedeem instead of redeem function since we've proved that the previewRedeem function 
// returns exactly the same value as the redeem function for a given input.

// owner can change claimable fee through setFee and withdrawFee to change the totalAssets which in 
// turn impacts the assets received by the user

// 
rule noFrontRunningInRedemption(method f)
    // filtered {f -> f.selector == redeem(uint256,address,address).selector}
    filtered { f -> !harnessOnlyMethods(f) && !f.isView }
{
    uint256 shares;
    address receiver;
    address owner;
    env e1;
    storage initState = lastStorage;
    require shares == 2;
    uint256 index = _SymbolicLendingPoolL1.getReserveNormalizedIncome(e1, Underlying);
    require index ==2;
    // user1 getting some assets for a given number of shares at initstorage
    // user previewRedeem instead
    uint256 assets1 = previewRedeem(shares);
    uint256 maxWithdrawable1 = maxAssetsWithdrawableFromAaveWrapper(e1);

    // some action by user2 at initStorage
    env e2;
    require e2.msg.sender != owner();
    calldataarg args;
    f(e2, args) at initState;
    
    require totalAssets(e2) != 0;
    require totalSupply() != 0;

    // user1 redeeming the same number of shares after user2 action
    uint256 maxWithdrawable2 = maxAssetsWithdrawableFromAaveWrapper(e1);
    require maxWithdrawable2 == maxWithdrawable1;
    uint256 assets2 = previewRedeem(shares);

    // asserting that user1 gets the same amount of assets with or without any action by user2
    assert assets1 == assets2,"users should not be front run during redeem";
}

// Deposit front-running: A user with a given number of shares should be able to redeem them for the same amount of assets
// regardless of actions by another user. The pupose of this rule is to check that the conversion ratio of shares into assets
// is not impacted by actions of another user

// requiring that totalSupply !=0 after the parametric call in order to avoid cases where returned shares amount is 
// equal to specified asset amount

// using previewDeposit instead of deposit function since we've proved that the previewDeposit function 
// returns exactly the same value as the deposit function for a given input.

// owner can change claimable fee through setFee and withdrawFee to change the totalAssets which in 
// turn impacts the assets received by the user

rule noFrontRunningInDeposit(method f)
filtered { f -> !harnessOnlyMethods(f) && !f.isView }
{
    uint256 assets;
    env e1;
    storage initState = lastStorage;    
    require assets == 2;
    // user1 getting some assets for a given number of shares at initstorage
    // user previewRedeem instead
    uint256 shares1 = previewDeposit(e1, assets);

    // some action by user2 at initStorage
    env e2;
    require e2.msg.sender != owner();
    calldataarg args;
    f(e2, args) at initState;

    require totalAssets(e2) != 0;
    require totalSupply() != 0;

    // user1 redeeming the same number of shares after user2 action
    uint256 shares2 = previewDeposit(e1, assets);

    // asserting that user1 gets the same amount of assets with or without any action by user2
    assert shares1 == shares2,"users should not be front run during redeem";
}



