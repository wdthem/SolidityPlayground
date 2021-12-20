from brownie import SimpleStorage, accounts, config


def read_contract():

    # 0 index is current deployment
    # -1 index is the most recent
    simple_storage = SimpleStorage[-1]
    # ABI
    # Address
    print(simple_storage.retrieve())


def main():
    read_contract()
