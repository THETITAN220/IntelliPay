// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AssetTransfer {
    // Owner of the contract
    address public owner;

    // Mapping to track asset balances
    mapping(address => uint256) public balances;

    // Events for transparency and tracking
    event Deposit(address indexed depositor, uint256 amount);
    event Withdrawal(address indexed recipient, uint256 amount);
    event Transfer(address indexed from, address indexed to, uint256 amount);

    // Modifier to restrict owner-only functions
    modifier onlyOwner() {
        require(msg.sender == owner, "Only contract owner can call this function");
        _;
    }

    // Constructor sets the contract deployer as owner
    constructor() {
        owner = msg.sender;
    }

    // Allow contract to receive Ether
    receive() external payable {
        deposit();
    }

    // Deposit function to add funds to the contract
    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    // Transfer assets between addresses
    function transferAsset(address to, uint256 amount) external {
        require(to != address(0), "Invalid recipient address");
        require(amount > 0, "Transfer amount must be greater than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;
        balances[to] += amount;

        emit Transfer(msg.sender, to, amount);
    }

    // Withdraw funds from the contract
    function withdraw(uint256 amount) external {
        require(amount > 0, "Withdrawal amount must be greater than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;
        
        // Transfer funds
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");

        emit Withdrawal(msg.sender, amount);
    }

    // Owner-only function to emergency withdraw all contract funds
    function emergencyWithdraw() external onlyOwner {
        uint256 contractBalance = address(this).balance;
        require(contractBalance > 0, "No funds to withdraw");

        (bool success, ) = payable(owner).call{value: contractBalance}("");
        require(success, "Emergency withdrawal failed");

        emit Withdrawal(owner, contractBalance);
    }

    // Check contract balance
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }

    // Check user's balance
    function getBalance() external view returns (uint256) {
        return balances[msg.sender];
    }
}