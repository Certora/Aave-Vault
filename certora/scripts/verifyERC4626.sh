certoraRun certora/harness/ATokenVaultHarness.sol \
    certora/harness/DummyContract.sol \
    certora/harness/pool/SymbolicLendingPoolL1.sol \
    certora/harness/tokens/DummyERC20_aTokenUnderlying.sol \
    certora/munged/lib/aave-v3-core/contracts/protocol/tokenization/AToken.sol \
    --verify ATokenVaultHarness:certora/specs/erc4626.spec \
    --link ATokenVaultHarness:AAVE_POOL=SymbolicLendingPoolL1 \
           ATokenVaultHarness:ATOKEN=AToken \
           ATokenVaultHarness:UNDERLYING=DummyERC20_aTokenUnderlying \
           ATokenVaultHarness:DUMMY=DummyContract \
           AToken:POOL=SymbolicLendingPoolL1 \
           SymbolicLendingPoolL1:underlyingToken=DummyERC20_aTokenUnderlying \
           SymbolicLendingPoolL1:aToken=AToken \
           AToken:_underlyingAsset=DummyERC20_aTokenUnderlying \
    --solc solc8.10 \
    --optimistic_loop \
    --staging pre_cvl2 \
    --packages @openzeppelin-upgradeable=certora/munged/lib/openzeppelin-contracts-upgradeable/contracts \
               @aave-v3-core=certora/munged/lib/aave-v3-core/contracts \
               @aave-v3-periphery=certora/munged/lib/aave-v3-periphery/contracts \
               @openzeppelin=certora/munged/lib/openzeppelin-contracts/contracts \
               @aave/core-v3=certora/munged/lib/aave-v3-core \
    --msg "$1" \
    --settings  -t=2000,-mediumTimeout=1200,-depth=15    \
    --send_only \
    --rule previewDepositAmountCheck \


#--typecheck_only

#    --method "mintWithATokens(uint256,address)" \
           
#    --rule must_not_revert \
           
#    --method "deposit(uint256,address)" \



#    --rule accumulated_fee_better \


    
#    --rule lastVaultBalance_OK_2 \

#    --rule inv_nonZero_shares_imply_nonZero_assets \




    


#    --rule larger_deposit_imply_more_shares \


    #--typecheck_only \





    
    #--method "withdrawWithSig(uint256,address,address,(uint8,bytes32,bytes32,uint256))"


#wrapped-atoken-vault complexity checks


