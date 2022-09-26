import csv
from eth_abi import encode
from merkle import MerkleTree
import random


def get_packed(el):
    return encode(["address", "uint256"], [el["address"], el["value"]])


def generate_bdei_tree():
    data = {}

    # generate 1000 random data, with address and value

    # generate 100 random eth address
    for i in range(100):
        address = "0x" + "".join([random.choice("0123456789abcdef") for i in range(40)])
        data[address] = random.randint(10000000000000000, 1000000000000000000000000)

    data["0x33da80ce59602c2d66da944392cdf95bd4928c5e"] = 1232423423432

    array_data = []
    for address, value in data.items():
        array_data.append({"address": address, "value": value})

    tree = MerkleTree(get_packed=get_packed, data=array_data)
    tree.generate_tree()
    return tree, data


if __name__ == "__main__":
    generate_bdei_tree()
