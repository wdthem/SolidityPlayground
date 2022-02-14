from scripts.helpful_scripts import (
    get_account,
    get_contract,
    fund_with_link,
    OPENSEA_URL,
)
from brownie import config, network, AdvancedCollectible


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )

    # fund with LINK so that we have the means to call a random number from VRFC  oordinator
    fund_with_link(advanced_collectible.address)
    tx = advanced_collectible.createCollectible({"from": account})
    tx.wait(1)
    print("New token has been created!")

    # also returning the transaction to make the request ID available to the unit test
    return advanced_collectible, tx


def main():
    deploy_and_create()
