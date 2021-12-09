from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3
from dotenv import load_dotenv

# load settings from .env file
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode

# walk down json
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get ABI

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# local ganache blockchain - same as Javascript VM in Remix
# connect via Web3

w3 = Web3(
    # change URL to network, localhost or test network
    # ganache-cli: http://127.0.0.1:8545
    # ganache-ui:  http://127.0.0.1:7545
    # rinkeby via infura acount: https://rinkeby.infura.io/v3/65fc66214b9448829943181bf61b13c5
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/65fc66214b9448829943181bf61b13c5")
)

# not the network ID.
# Seems hard-coded in Ganache to 1337
# rinkeby is 4
chain_id = 4

# change address to whatever required for the network you are running on
my_address = "0x9329C226257DEb4BfE94Df8a4A4aaB18F4F7cA42"

# note: python requires you to add the 0x to the beginning of the private key
# but you don't see this in ganache
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# build a transaction
# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

# sign transaction
signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# send transaction
print("Deploying contract...")
send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
print("Deployed!")

# working with the contract
# contract address
# contract abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call => simulate making the call and getting a return value - NO STATE CHANGE
# transact => actually make a state change

# initial value of favoriteNumber
print(simple_storage.functions.retrieve().call())

print("Updating contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")
print(simple_storage.functions.retrieve().call())
