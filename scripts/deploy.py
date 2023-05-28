#!/usr/bin/python3
from brownie import interface, Token, web3, chain
from scripts.helpful_scripts import get_account


def approve(token, _from, to: str, amount: str):
    token.approve(to, amount, {"from": _from})


def addL(router, owner, first: str, second: str, aF: int, aS: int):
    router.addLiquidity(
        first,
        second,
        aF,
        aS,
        aF,
        aS,
        owner,
        # web3.eth.getBlock("latest")["timestamp"]
        # just to be safe
        chain.time() + 10000,
        {"from": owner},
    )


# setup
def deploy():
    owner, attacker = get_account()
    tokens = []

    router = interface.ISwapV2Router02("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")

    # print(dir(router))
    # mint new tokens
    print("Minting tokens...")
    Atoken = Token.deploy("Atoken", "ATK", "100 ether", {"from": owner})
    Btoken = Token.deploy("Btoken", "BTK", "100 ether", {"from": owner})
    Ctoken = Token.deploy("Ctoken", "CTK", "100 ether", {"from": owner})
    Dtoken = Token.deploy("Dtoken", "DTK", "100 ether", {"from": owner})
    Etoken = Token.deploy("Etoken", "ETK", "100 ether", {"from": owner})
    tokens.append(Atoken)
    tokens.append(Btoken)
    tokens.append(Ctoken)
    tokens.append(Dtoken)
    tokens.append(Etoken)

    # print(tokens)
    print("Approving tokens...")
    # Atoken.approve(router, "100 ether", {"from": owner})
    # Btoken.approve(router, "100 ether", {"from": owner})
    # Ctoken.approve(router, "100 ether", {"from": owner})
    # Dtoken.approve(router, "100 ether", {"from": owner})
    # Etoken.approve(router, "100 ether", {"from": owner})
    for token in tokens:
        approve(token, owner, router, "100 ether")

    # add liquidity
    print("Addding Liquidity...")
    addL(
        router, owner, Atoken, Btoken, web3.toWei(17, "ether"), web3.toWei(10, "ether")
    )
    addL(router, owner, Atoken, Ctoken, web3.toWei(11, "ether"), web3.toWei(7, "ether"))
    addL(router, owner, Atoken, Dtoken, web3.toWei(15, "ether"), web3.toWei(9, "ether"))
    addL(router, owner, Atoken, Etoken, web3.toWei(21, "ether"), web3.toWei(5, "ether"))
    addL(router, owner, Btoken, Ctoken, web3.toWei(36, "ether"), web3.toWei(4, "ether"))
    addL(router, owner, Btoken, Dtoken, web3.toWei(13, "ether"), web3.toWei(6, "ether"))
    addL(router, owner, Btoken, Etoken, web3.toWei(25, "ether"), web3.toWei(3, "ether"))
    addL(
        router, owner, Ctoken, Dtoken, web3.toWei(30, "ether"), web3.toWei(12, "ether")
    )
    addL(router, owner, Ctoken, Etoken, web3.toWei(10, "ether"), web3.toWei(8, "ether"))
    addL(
        router, owner, Dtoken, Etoken, web3.toWei(60, "ether"), web3.toWei(25, "ether")
    )

    print("Giving attacker 5 Btokens...")
    Btoken.transfer(attacker, web3.toWei(5, "ether"), {"from": owner})

    return owner, router, tokens, attacker


def main():
    deploy()
