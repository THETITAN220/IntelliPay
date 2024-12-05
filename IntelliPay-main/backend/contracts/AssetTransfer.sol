// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


 
  contract AssetTransfer {
      event Transfer(address indexed from, address indexed to, uint256 amount);

      function transfer(address to) public payable {
          require(msg.sender != to, "Sender and recipient cannot be the same");
          require(msg.value > 0, "Transfer amount must be greater than 0");
          (bool sent, ) = to.call{value: msg.value}("");
          require(sent, "Failed to send Ether");

          emit Transfer(msg.sender, to, msg.value);
      }
  } 