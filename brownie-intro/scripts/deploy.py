from brownie import accounts, config

def deploy_simple_storage():
    account = accounts.add(config["wallets"]["from_key"])
    print(account)

def main() -> None:
    print("hello, brownie!")
    deploy_simple_storage()
