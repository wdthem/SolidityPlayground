// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyHash;
    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    function enter() public payable {
        // $50 minimum
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();

        //convert price to uint256
        //price feed already returns 8 decimals, so add 10 more
        uint256 adjustedPrice = uint256(price) * 10**10;

        // $50, $2,000 / ETH
        // 50/2000
        // 50 * 10000somebignumber / 2000
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;

        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start new lottery yet"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        //quick and dirty for pseudo random - NOT FOR PROD
        // hash a global variable
        //uint256(
        //    keccak256(
        //        abi.encodePacked(
        //            nonce, //predictable (aka tx number)
        //            msg.sender, //predictable
        //            block.difficulty, //can actually be manipulated by miners!
        //            block.timestamp //predictable
        //        )
        //    )
        //) % players.length; //this selects the winner from the array based on the random number
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;

        //from imported VRFConsumerBase.sol
        //calls chainlink node and pays link token fee
        bytes32 requestId = requestRandomness(keyHash, fee); 

        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "You aren't there yet!"
        );
        require(_randomness > 0, "random-not-found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        // Reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
