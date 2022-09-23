import csv
import json
from eth_abi import encode
from merkle import MerkleTree


def get_packed(el):
    print(el)
    return encode(['uint256', 'uint256'], [el['tokenId'], el['amount']])


def generate_nft_tree():
    data = {}
    with open('nft_data.json') as file:
        spreadsheet = list(csv.reader(file))

    # todo replace real data
    array_data = []
    for i in range(1000):
        data[i] = 25719935892000620225346
        array_data.append({
            'tokenId': i,
            'amount': 25719935892000620225346
        })

    tree = MerkleTree(get_packed=get_packed, data=array_data)
    tree.generate_tree()
    return tree, data


if __name__ == '__main__':
    generate_nft_tree()
