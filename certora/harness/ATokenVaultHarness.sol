// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import {ATokenVault} from "../munged/src/ATokenVault.sol";
import {IPoolAddressesProvider} from "@aave-v3-core/interfaces/IPoolAddressesProvider.sol";
import {DummyContract} from "./DummyContract.sol";
import {MathUpgradeable} from "@openzeppelin-upgradeable/utils/math/MathUpgradeable.sol";



/**
 * @title ATokenVault
 * @author Aave Protocol
 * @notice An ERC-4626 vault for Aave V3, with support to add a fee on yield earned.
 */
contract ATokenVaultHarness is ATokenVault {
    using MathUpgradeable for uint256;using MathUpgradeable for uint256;
    DummyContract DUMMY;
    
    constructor(address underlying, uint16 referralCode, IPoolAddressesProvider poolAddressesProvider) ATokenVault(underlying, referralCode, poolAddressesProvider) {
    }
    
    function havoc_all() public {
        DUMMY.havoc_all_dummy();
    }
    
    function accrueYield() external {
        _accrueYield();
    }
    
    function getAccumulatedFees() external returns(uint128) {
        return _s.accumulatedFees;
    }

    function mulDivWrapper(uint256 x, uint256 y, uint256 deno, uint8 rounding) external returns(uint256 result){

        result = x.mulDiv(y,deno,MathUpgradeable.Rounding.Down);
    }

    function maxAssetsWithdrawableFromAaveWrapper() external returns (uint256){
        return _maxAssetsWithdrawableFromAave();
    }


}
