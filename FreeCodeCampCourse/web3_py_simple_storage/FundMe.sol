//SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    //prevent integer wrapping on overflow - required for solidity prior to 0.8
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;

    //constructor
    constructor() public {
        owner = msg.sender;
    }

    //this function can be used to pay for things
    function fund() public payable {
        //$5
        uint256 minimumUsd = 5 * 10**18;
        require(
            getConversionRate(msg.value) >= minimumUsd,
            "You need to spend more ETH!"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        //what the ETH => USD conversion rate
        funders.push(msg.sender); //ignore the redundanchy risk for purpose of example
    }

    function getVersion() public view returns (uint256) {
        //ETH / USD address from here: https://docs.chain.link/docs/ethereum-addresses/
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        //ETH / USD address from here: https://docs.chain.link/docs/ethereum-addresses/
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );

        //blanked out params to avoid compiler warnings on unused parameters
        (, int256 price, , , ) = priceFeed.latestRoundData();

        //return price with 18 decimal places, in USD, to match the 18 decimal places of WEI, for consistency
        //WEI is the smallest possible unit of measure
        //price has 8 decimal places, (can be confirmed via decimals method on interface) so add 10
        return uint256(price * 10000000000);
    }

    //1000000000 WEI = 1 GWEI. Example assuming they send in WEI  equivalent of 1 GWEI
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();

        //to get correct amount, divide by number with 18 zeroes which is the number of decimal places of WEI
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;

        //function returns 4424470000000 (or whatever current value is)
        //this number still needs 18 decimals places, so it is really
        //0.000004424470000000, so this is 1 GWEI in USD
        //if multiplied by the GWEI equivalent of 1 ETH, we get
        //4,424.47 - the amount in USD
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _; //this indicates "run the rest of the code the function is modifying"
    }

    //withdraw only available to contract owner
    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);

        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        funders = new address[](0);
    }
}
