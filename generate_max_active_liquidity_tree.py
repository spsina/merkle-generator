import csv
from eth_abi import encode
from merkle import MerkleTree
import random


def get_packed(el):
    return encode(["address", "uint256"], [el["address"], el["value"]])


def generate_tree():
    data = {}

    # load max active liquidity data from csv
    with open("max_active_liquidity.csv") as file:
        spreadsheet = list(csv.reader(file))
        for row in spreadsheet[1:]:
            address = row[0]
            value = int(float(row[1].replace(",", "")) * 1e18)
            data[address] = value

    array_data = []
    for address, value in data.items():
        array_data.append({"address": address, "value": value})

    tree = MerkleTree(get_packed=get_packed, data=array_data)
    tree.generate_tree()
    return tree, data


if __name__ == "__main__":
    generate_tree()
