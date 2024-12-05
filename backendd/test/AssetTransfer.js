const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AssetTransfer", function () {
    let contract, owner, sender, recipient;

    beforeEach(async function () {
        [owner, sender, recipient] = await ethers.getSigners();
        const AssetTransfer = await ethers.getContractFactory("AssetTransfer");
        contract = await AssetTransfer.deploy();
        await contract.deployed();
    });

    it("Should allow depositing funds", async function () {
        const depositAmount = ethers.parseEther("0.5");
        
        await expect(contract.connect(sender).deposit({
            value: depositAmount
        })).to.emit(contract, "Deposit")
           .withArgs(sender.address, depositAmount);

        const balance = await contract.balances(sender.address);
        expect(balance).to.equal(depositAmount);
    });

    it("Should transfer assets between accounts", async function () {
        const depositAmount = ethers.utils.parseEther("1");
        
        // Deposit funds
        await contract.connect(sender).deposit({ value: depositAmount });

        // Transfer
        await expect(contract.connect(sender).transferAsset(recipient.address, depositAmount))
            .to.emit(contract, "Transfer")
            .withArgs(sender.address, recipient.address, depositAmount);

        const senderBalance = await contract.balances(sender.address);
        const recipientBalance = await contract.balances(recipient.address);

        expect(senderBalance).to.equal(0);
        expect(recipientBalance).to.equal(depositAmount);
    });

    it("Should allow withdrawal", async function () {
        const depositAmount = ethers.utils.parseEther("1");
        
        // Deposit funds
        await contract.connect(sender).deposit({ value: depositAmount });

        // Track initial balance
        const initialBalance = await sender.getBalance();

        // Withdraw
        await expect(contract.connect(sender).withdraw(depositAmount))
            .to.emit(contract, "Withdrawal")
            .withArgs(sender.address, depositAmount);

        const finalBalance = await sender.getBalance();
        expect(finalBalance).to.be.above(initialBalance);
    });

    it("Should prevent invalid transfers", async function () {
        const transferAmount = ethers.utils.parseEther("1");

        await expect(
            contract.connect(sender).transferAsset(recipient.address, transferAmount)
        ).to.be.revertedWith("Insufficient balance");

        await expect(
            contract.connect(sender).transferAsset(ethers.constants.AddressZero, transferAmount)
        ).to.be.revertedWith("Invalid recipient address");
    });
});