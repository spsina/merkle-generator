import binascii
from multiprocessing.sharedctypes import Value
from flask import Flask
from flask_cors import CORS

from generate_max_active_liquidity_tree import generate_tree

# dei_tree, dei_data = generate_dei_tree()
tree, data = generate_tree()

app = Flask(__name__)
CORS(app)


@app.route("/root/")
def get_root():
    for _, node in tree.tree.items():
        if node["parent"] is None:
            return {"root": binascii.hexlify(node["hash"]).decode()}


@app.route("/proof/<address>/")
def get_proof(address):
    value = data[address]

    el = {
        "address": address,
        "value": value,
    }
    print(el)
    proof = tree.get_proof(el)
    proof = ["0x" + binascii.hexlify(p).decode() for p in proof]
    print(proof)
    result = {
        "proof": proof,
        "value": value,
    }
    return result
