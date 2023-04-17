certoraRun src/ATokenVault.sol \
    certora/harness/pool/SymbolicLendingPoolL1.sol \
    certora/harness/tokens/DummyERC20_aTokenUnderlying.sol \
    lib/aave-v3-core/contracts/protocol/tokenization/AToken.sol \
    --verify ATokenVault:certora/specs/basic.spec \
    --link ATokenVault:AAVE_POOL=SymbolicLendingPoolL1 \
           ATokenVault:ATOKEN=AToken \
           ATokenVault:UNDERLYING=DummyERC20_aTokenUnderlying \
           AToken:POOL=SymbolicLendingPoolL1 \
           SymbolicLendingPoolL1:underlyingToken=DummyERC20_aTokenUnderlying \
           SymbolicLendingPoolL1:aToken=AToken \
           AToken:_underlyingAsset=DummyERC20_aTokenUnderlying \
    --solc solc8.10 \
    --optimistic_loop \
    --staging pre_cvl2 \
    --packages @openzeppelin-upgradeable=lib/openzeppelin-contracts-upgradeable/contracts \
               @aave-v3-core=lib/aave-v3-core/contracts \
               @aave-v3-periphery=lib/aave-v3-periphery/contracts \
               @openzeppelin=lib/openzeppelin-contracts/contracts \
    --msg "$1" \
    --settings  -t=1400,-mediumTimeout=800,-depth=15    \
    --send_only \
    --rule inv_nonZero_shares_imply_nonZero_assets \
    --method "deposit(uint256,address)" \


#    --rule accumulated_fee \





    


#    --rule larger_deposit_imply_more_shares \


    #--typecheck_only \





    
    #--method "withdrawWithSig(uint256,address,address,(uint8,bytes32,bytes32,uint256))"


#wrapped-atoken-vault complexity checks


