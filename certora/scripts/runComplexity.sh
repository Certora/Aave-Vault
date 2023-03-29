certoraRun src/ATokenVault.sol \
    certora/harness/SymbolicLendingPoolL1.sol \
    certora/harness/DummyERC20_aTokenUnderlying.sol \
    lib/aave-v3-core/contracts/protocol/tokenization/AToken.sol \
    --verify ATokenVault:certora/specs/complexity.spec \
    --link ATokenVault:AAVE_POOL=SymbolicLendingPoolL1 \
           AToken:POOL=SymbolicLendingPoolL1 \
           ATokenVault:ATOKEN=AToken \
           ATokenVault:UNDERLYING=DummyERC20_aTokenUnderlying \
    --solc solc8.10 \
    --optimistic_loop \
    --staging  \
    --packages @openzeppelin-upgradeable=lib/openzeppelin-contracts-upgradeable/contracts \
               @aave-v3-core=lib/aave-v3-core/contracts \
               @aave-v3-periphery=lib/aave-v3-periphery/contracts \
               @openzeppelin=lib/openzeppelin-contracts/contracts \
    --msg "$1" \
    --send_only \
    --rule sanity \


    #--method "maxWithdraw(address)"


#wrapped-atoken-vault complexity checks


