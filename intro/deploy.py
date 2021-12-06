import json
from web3 import Web3
from solcx import compile_standard, install_solc


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_src = file.read()

# install solcx
install_solc("0.8.0")

# compile the source
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_src}},
        "settings": 
        {
            "outputSelection": 
            {
                "*": 
                {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    }, 
    solc_version = "0.8.0"
)

with open("./out.json", "w") as file:
    json.dump(compiled_sol, file)

# getting the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# getting the abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x02ECDdb09504C4d4B2ba2c7Ec80d77d44f6e631c"
private_key = "0xa9ddbecce894fdad11cd9864d9c58f794d23bd5f0d78d1c2eea204b284edfefc"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest test transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. Build a transaction
# 2. Sing the transaction
# 3. Send the transaction
transaction = SimpleStorage.constructor().buildTransaction({"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce})
signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# confirm transaction is received
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("tx_hash=", tx_hash)
print("receipt=", tx_receipt)

# working on-chain
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).buildTransaction({
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1
    }
)

singed_store_transaction = w3.eth.account.sign_transaction(store_transaction, private_key)
store_transaction_hash = w3.eth.send_raw_transaction(singed_store_transaction.rawTransaction)
store_transaction_receipt = w3.eth.wait_for_transaction_receipt(store_transaction_hash)
