import binascii
from flask import Flask
from flask_cors import CORS

from generate_tree import generate_tree

app = Flask(__name__)
CORS(app)

tree, data = generate_tree()


@app.route("/migration/root/")
def get_root():
    for _, node in tree.tree.items():
        if node["parent"] is None:
            return {"root": binascii.hexlify(node["hash"]).decode()}


@app.route("/migration/proof/<address>/")
def get_proof(address):
    address = address.lower()
    amount = data.get(address, None)
    proof = []
    if amount is not None:
        el = {
            "address": address,
            "amount": amount,
        }
        proof = tree.get_proof(el)
        proof = ["0x" + binascii.hexlify(p).decode() for p in proof]

    return {
        "proof": proof,
        "amount": str(amount),
    }

