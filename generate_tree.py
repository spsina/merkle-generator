import json
from eth_abi import encode
from merkle import MerkleTree


def get_packed(el):
    return encode(['uint256', 'uint256'], [int(el['tokenId']), int(el['amount'])])


def generate_tree():
    data = json.loads(open("data.json").read())
    array_data = []

    for key, amount in data.items():
        array_data.append({"tokenId": key, "amount": int(amount)})

    tree = MerkleTree(get_packed=get_packed, data=array_data)
    tree.generate_tree()
    return tree, data


if __name__ == '__main__':
    generate_tree()
