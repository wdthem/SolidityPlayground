// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    constructor() public ERC721("Doggie", "DOG") {
        tokenCounter = 0;
    }

    function createCollectible(string memory tokenUri)
        public
        returns (uint256)
    {
        //assign new token ID to new owner

        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenUri);
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }
}
