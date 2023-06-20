certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/erc4626-previewOPERATIONS.conf    

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/totalSupply_EQ_sumAllBal.conf

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/changeInContractBalanceShouldCauseAccrual.conf

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/rayMul_rayDiv_mulDiv_properties.conf    

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/lastVaultBalance_LEQ_ATokenBalThis.conf    

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/fees_LEQ_ATokenBal.conf   

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/positiveSupply_imply_positiveAssets-mint.conf    

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/positiveSupply_imply_positiveAssets-deposit.conf    

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/positiveSupply_imply_positiveAssets-withdraw.conf    

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/positiveSupply_imply_positiveAssets-redeem.conf   

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/positiveSupply_imply_positiveAssets-other.conf    

certoraRun --send_only --prover_version shelly/wowtimeout certora/conf/accrueYieldCheck.conf
