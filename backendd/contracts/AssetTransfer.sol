// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract AssetTransfer {
    address public owner;

    event TransferInitiated(address indexed from, address indexed to, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    function transferAsset(address payable to, uint256 amount) external payable {
        require(msg.value == amount, "Insufficient amount sent");
        require(to != address(0), "Invalid recipient address");

        to.transfer(amount);

        emit TransferInitiated(msg.sender, to, amount);
    }
}