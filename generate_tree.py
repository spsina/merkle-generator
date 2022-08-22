import json

from merkle import MerkleTree


def generate_tree():
    data = json.loads(open("data.json").read())
    array_data = []

    for key, amount in data.items():
        array_data.append({"tokenId": key, "amount": int(amount)})

    tree = MerkleTree(array_data)
    tree.generate_tree()

    return tree, data


if __name__ == '__main__':
    generate_tree()
