import json

from merkle import MerkleTree

data = json.loads(open("data.json").read())
array_data = []

for key, amount in data.items():
    array_data.append({"tokenId": key, "amount": int(amount)})

tree = MerkleTree(array_data)
tree.generate_tree()

result = open("tree.txt", "w")
result.write(json.dumps(tree.tree))
result.close()
