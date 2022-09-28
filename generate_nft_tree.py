import csv
from datetime import date, datetime
import json
from eth_abi import encode
from merkle import MerkleTree


def get_packed(el):
    return encode(
        ["uint256", "uint256", "uint256"],
        [el["tokenId"], el["amount"], el["maturity_time"]],
    )


def generate_nft_tree():
    data = {}
    array_data = []

    with open("nft_data.json") as file:
        data = json.load(file)
        for row in data:
            element_data = row
            data[row["tokenId"]] = element_data
            array_data.append(element_data)

    # todo replace real data
    # for i in range(1000):
    #     element_data = {
    #         "tokenId": i,
    #         "amount": int(25719935892000620225346),
    #         "maturity_date": int(1666572520),
    #     }

    #     data[i] = element_data
    #     array_data.append(element_data)

    tree = MerkleTree(get_packed=get_packed, data=array_data)
    tree.generate_tree()
    return tree, data


if __name__ == "__main__":
    generate_nft_tree()
