#!/usr/bin/python3
from brownie import accounts


def get_account():
    return accounts[0], accounts[1]
