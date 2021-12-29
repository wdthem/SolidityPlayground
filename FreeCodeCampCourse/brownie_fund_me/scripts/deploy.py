from brownie import FundMe, MockV3Aggregator, accounts, network, config
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # pass price feed address to our fundme contract

    # if we are on a persistent network like rinkeby, use the assocated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed_address"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    # the above call to .get won't fail if you forget to add the key to config

    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
