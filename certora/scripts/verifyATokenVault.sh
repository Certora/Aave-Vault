
if [[ "$1" ]]
then
    RULE="--rule $1"
fi

if [[ "$2" ]]
then
    MSG="- $2"
fi
certoraRun certora/harness/ATokenVaultHarness.sol \
    certora/harness/pool/SymbolicLendingPoolL1.sol \
    certora/harness/tokens/DummyERC20_aTokenUnderlying.sol \
    certora/munged/lib/aave-v3-core/contracts/protocol/tokenization/AToken.sol \
    --verify ATokenVaultHarness:certora/specs/ATokenVault.spec \
    --link ATokenVaultHarness:AAVE_POOL=SymbolicLendingPoolL1 \
            ATokenVaultHarness:ATOKEN=AToken \
            ATokenVaultHarness:UNDERLYING=DummyERC20_aTokenUnderlying \
            SymbolicLendingPoolL1:underlyingToken=DummyERC20_aTokenUnderlying \
            SymbolicLendingPoolL1:aToken=AToken \
            AToken:POOL=SymbolicLendingPoolL1 \
            AToken:_underlyingAsset=DummyERC20_aTokenUnderlying \
    --solc solc8.10 \
    --optimistic_loop \
    --cloud \
    --packages @openzeppelin-upgradeable=certora/munged/lib/openzeppelin-contracts-upgradeable/contracts \
               @aave-v3-core=certora/munged/lib/aave-v3-core/contracts \
               @aave-v3-periphery=certora/munged/lib/aave-v3-periphery/contracts \
               @openzeppelin=certora/munged/lib/openzeppelin-contracts/contracts \
               @aave/core-v3=certora/munged/lib/aave-v3-core \
    --send_only \
        $RULE \
    --rule_sanity basic \
    --msg "ATokenVault - $RULE $MSG  "

            # AToken:_incentivesController=RewardsControllerHarness \

    # --rule inv_atoken_scaled_balanceOf_leq_totalSupply \
    #--typecheck_only \


    #--method "withdrawWithSig(uint256,address,address,(uint8,bytes32,bytes32,uint256))"


#wrapped-atoken-vault complexity checks


