// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

library Errors {
    // Vault Errors
    error FeeTooHigh();
    error InsufficientFees();
    error AssetNotSupported();

    // MetaTx Lib Errrors
    error SignatureExpired();
    error SignatureInvalid();
}