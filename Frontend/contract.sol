// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MoneyStorage is ERC20 {
    address public owner;
    uint256 public amount = 0;
    IERC20 public testCoin;

    uint8 private _decimals = 2;

    constructor(address _tokenAddress) ERC20("TestCoin", "T1") {
        owner = msg.sender;
        _mint(msg.sender, 1000000 * 10 ** _decimals);
        testCoin = IERC20(_tokenAddress); 
    }
    function decimals() public view virtual override returns (uint8) {
        return _decimals;
    }

}
