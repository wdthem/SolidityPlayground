from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, config, network

import time


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth-usd-price-feed-address").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        # built-in contstructor params
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]

    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)  # needed for Brownie
    print("The lottery is started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = (
        lottery.getEntranceFee() + 100000000
    )  # just add some wei to make sure we meet the minimum
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]

    # need link token - fund the contract
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)
    print("Lottery ended!")
    time.sleep(60)

    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
