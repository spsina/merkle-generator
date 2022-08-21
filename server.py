from flask import Flask
from merkle import MerkleTree

tree = MerkleTree().load_from_file("tree.txt")

app = Flask(__name__)


@app.route("/<tokenId>/<amount>/")
def get_proof(tokenId, amount):
    return tree.get_proof({"tokenId": tokenId, "amount": int(amount)})


@app.route("/root")
def get_root():
    return {"root": tree.root}
