import csv
import json

from web3 import Web3
from multicall import Multicall, Call

w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/fantom/bb16818498f786afd5eef9dae23804758f6c2e56149fb762ec5beea68a45646c'))

OXD = "0xc5A9848b9d145965d821AaeC8fA32aaEE026492d"
oxSOLID = "0xDA0053F0bEfCbcaC208A3f867BB243716734D809"
SEX = "0xD31Fcd1f7Ba190dBc75354046F6024A9b86014d7"
SOLIDsex = "0x41adAc6C1Ff52C5e27568f27998d747F7b69795B"

tokens = [OXD, oxSOLID, SEX, SOLIDsex]

contract_address = "0x15D5823b33Ad6c272274a8Dc61E617153AB1da1D"

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"


def process_delegations():
    with open('delegation_result.json', 'r') as file:
        total_delegations = json.loads(file.read())

    addresses = []
    for token in tokens:
        addresses += total_delegations[token].keys()
    addresses = list(set(addresses))

    delegations = [["Address", "Delegated Address"]]
    # check if there is conflict in delegations
    for address in addresses:
        delegation_address = ZERO_ADDRESS
        for token in tokens:
            a = total_delegations[token].get(address)
            if a:
                delegation_address = a
                continue
        delegations.append([address, delegation_address])

    with open('delegations.csv', 'w', newline='') as file:
        csv.writer(file).writerows(delegations)


def main():
    with open('data.csv') as file:
        rows = list(csv.reader(file))

    total_delegations = {}
    for token in tokens:
        delegations = {}

        print('\n', token, ':')
        calls = []
        for row in rows[1:]:
            user_address = row[0]

            if not user_address.startswith('0x'):
                continue

            user_address = w3.toChecksumAddress(user_address)

            call = Call(
                w3,
                contract_address,
                ["erc20Beneficiaries(address,address)(address)", user_address, token],
                [[user_address, None]]
            )
            calls.append(call)

        multicall = Multicall(w3, calls)
        result = multicall()

        for user_address, delegated_address in result.items():
            delegated_address = delegated_address[0]
            if delegated_address != ZERO_ADDRESS:
                print(' - ', user_address, ' => ', delegated_address)
                delegations[user_address] = delegated_address

        total_delegations[token] = delegations

    with open('delegation_result.json', 'w') as file:
        file.write(json.dumps(total_delegations))

    process_delegations()


if __name__ == '__main__':
    main()
