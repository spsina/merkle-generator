from flask import Flask
from merkle import MerkleTree

tree = MerkleTree().load_from_file("tree.txt")

app = Flask(__name__)

@app.route("/root/")
def get_root():
    for _, node in tree.tree.items():
        if node['parent'] is None:
            return {
                'root': node['hash']
            }

@app.route("/proof/<tokenId>/<amount>/")
def get_proof(tokenId, amount):
    return tree.get_proof({'tokenId': tokenId, 'amount': int(amount)})
