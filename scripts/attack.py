#!/usr/bin/python3
from brownie import web3, chain
from scripts.helpful_scripts import get_account
from scripts.deploy import deploy, approve
from scripts.generate_path import generate_path
from colorama import Fore
from random import shuffle


# * colours
green = Fore.GREEN
red = Fore.RED
blue = Fore.BLUE
magenta = Fore.MAGENTA
reset = Fore.RESET


def getAmountsOut(router, amount: int, path: list) -> tuple:
    return router.getAmountsOut(amount, path)


def swap(router, attacker, amount: int, path: list) -> int:
    tx = router.swapExactTokensForTokens(
        amount,
        1,
        path,
        attacker,
        chain.time() + 10000,
        {"from": attacker},
    )
    swappedAmount = int(web3.eth.getTransactionReceipt(tx.txid)["logs"][2]["data"], 16)
    # print(tx.return_value)

    return swappedAmount


def attack():
    owner, router, tokens, attacker = deploy()
    NODES = {
        "A": tokens[0],
        "B": tokens[1],
        "C": tokens[2],
        "D": tokens[3],
        "E": tokens[4],
    }

    print(f"{green}Approving tokens from attacker{reset}")
    for token in tokens:
        approve(token, attacker, router, "5 ether")

    initial_attacker_balance = tokens[1].balanceOf(attacker)

    possible_paths = generate_path()

    # shuffle the paths for fun i.e. to test different paths
    shuffle(possible_paths)
    shuffle(possible_paths)
    shuffle(possible_paths)

    print(f"{red}Possible paths{reset}")
    # print(possible_paths)

    # path = []
    # path.append(tokens[1])
    # path.append(tokens[0])
    for path in possible_paths:
        if len(path) == 1:
            # skip the path
            continue

        # add token 'B' at the end as it's our final goal
        path = list(path)
        path.append("B")

        print(f"{green}Checking path: {magenta}{'->'.join(path)}{reset}")

        swaps = []
        # path = ("B", "D", "C", "B")
        for i in path:
            swaps.append(NODES.get(i))
        # print(swaps)
        # swaps.append(NODES.get("B"))

        swap_result = getAmountsOut(router, initial_attacker_balance, swaps)

        balance_before_swap = swap_result[0]
        balance_after_swap = swap_result[-1]

        if balance_after_swap > balance_before_swap:
            swap(router, attacker, initial_attacker_balance, swaps)

            print(f"{blue}Balance before swap: {green}{balance_before_swap}")
            print(f"{blue}Balance after swap : {red}{tokens[1].balanceOf(attacker)}")

            assert balance_after_swap > initial_attacker_balance

            print(f"{red}Followed path: {green}{'->'.join(path)}{reset}")
            exit(0)


def main():
    attack()


if __name__ == "__main__":
    main()
