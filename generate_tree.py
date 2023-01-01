import csv
import decimal
import json

from eth_abi import encode

from merkle import MerkleTree


def convert_data():
    data = {}
    with open('data.csv') as file:
        rows = list(csv.reader(file))

        for row in rows[1:]:
            address = row[0].lower()
            if address.startswith('0x'):
                amount = int(decimal.Decimal(row[1]) * int(1e18))
                if amount != 0:
                    data[address] = amount

    with open('delegations.csv', 'r') as file:
        delegations = list(csv.reader(file))

    for address, to in delegations[1:]:
        address = address.lower()
        to = to.lower()
        amount = data.get(address, 0) + data.get(to, 0)
        del data[address]
        data[to] = amount

    # for front
    with open('data.json', 'w') as file:
        json.dump(data, file)

    # for non devs
    with open('delegated_data.csv', 'w', newline='') as file:
        csv_data = [
            ["Address", "Amount (scaled)", "Amount (1e18)"]
        ]
        for address, amount in data.items():
            csv_data.append([address, amount / 1e18, amount])
        csv.writer(file).writerows(csv_data)

    return data


def get_packed(el):
    return encode(['address', 'uint256'], [el['address'], int(el['amount'])])


def generate_tree():
    data = convert_data()

    array_data = []
    for key, amount in data.items():
        array_data.append({"address": key, "amount": amount})

    tree = MerkleTree(get_packed=get_packed, data=array_data)
    tree.generate_tree()

    return tree, data


if __name__ == '__main__':
    generate_tree()
