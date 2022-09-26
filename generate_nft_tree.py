import csv
from datetime import date, datetime
import json
from eth_abi import encode
from merkle import MerkleTree


def get_packed(el):
    print(el)
    return encode(
        ["uint256", "uint256", "uint256"],
        [el["tokenId"], el["amount"], el["maturity_date"]],
    )


def generate_nft_tree():
    data = {}
    array_data = []

    # with open('nft_data.json') as file:
    #     spreadsheet = list(csv.reader(file))
    #     for row in spreadsheet[1:]:
    #         element_data = {
    #             'tokenId': int(row[0]),
    #             'amount': int(row[1]),
    #             'maturity_date': int(row[2])
    #         }
    #         data[int(row[0])] = element_data
    #         array_data.append(element_data)

    # todo replace real data
    for i in range(1000):
        element_data = {
            "tokenId": i,
            "amount": int(25719935892000620225346),
            "maturity_date": int(1666572520),
        }

        data[i] = element_data
        array_data.append(element_data)

    tree = MerkleTree(get_packed=get_packed, data=array_data)
    tree.generate_tree()
    return tree, data


if __name__ == "__main__":
    generate_nft_tree()
