from brownie import network, config, accounts

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork"]


def get_account(index=None, id=None):

    # account = accounts[0] # first account generated by ganache-cli
    # account = accounts.load("freecodecamp-account")  # account manually generated in brownie, will prompt for password
    # account = accounts.add(config["wallets"]["from_key"]) # account based on private key in .env
    # print(account)

    # interrogate network list, accessible via "brownie networks list"
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]  # first account generated by ganache-cli

    return accounts.add(config["wallets"]["from_key"])
