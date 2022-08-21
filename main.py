import imp
from merkle import MerkleTree
from pprint import pprint
d =   {'name': 'sina'},

data = [
   d,
    {'name': "kazem"},
    {'name': "saEdi"},
    {'name': "mmd"},
]

tree = MerkleTree(data)
tree.generate_tree()

pprint(tree.tree)
proof = tree.get_proof(d)
pprint(proof)
print(tree.verify(d, proof))