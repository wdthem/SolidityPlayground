# current price of Ethereum
# 0.0093
# 090000000000000000
from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth-usd-price-feed-address"],
        {"from": account},
    )

    assert lottery.getEntranceFee() > Web3.toWei(0.008, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.098, "ether")
