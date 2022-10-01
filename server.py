import binascii
from flask import Flask
from flask_cors import CORS
from generate_nft_tree import generate_nft_tree
from generate_max_active_liquidity_tree import generate_tree

app = Flask(__name__)
CORS(app)

nft_tree, nft_data = generate_nft_tree()


@app.route("/nft/root/")
def get_nft_root():
    for _, node in nft_tree.tree.items():
        if node["parent"] is None:
            return {"root": binascii.hexlify(node["hash"]).decode()}


@app.route("/nft/proof/<token_id>/")
def get_nft_proof(token_id):
    token_id = int(token_id)
    token_data = nft_data[token_id]
    maturity_date = token_data["maturity_time"]
    amount = token_data["amount"]

    el = {
        "tokenId": token_id,
        "amount": amount,
        "maturity_time": maturity_date,
    }

    proof = nft_tree.get_proof(el)
    proof = ["0x" + binascii.hexlify(p).decode() for p in proof]

    result = {
        "proof": proof,
        "value": {
            "tokenId": token_id,
            "amount": str(amount),
            "maturity_time": maturity_date,
        },
    }
    return result


tree, data = generate_tree()


@app.route("/liquidity/root/")
def get_root():
    for _, node in tree.tree.items():
        if node["parent"] is None:
            return {"root": binascii.hexlify(node["hash"]).decode()}


@app.route("/liquidity/proof/<address>/")
def get_proof(address):
    value = data[address]

    el = {
        "address": address,
        "value": value,
    }
    proof = tree.get_proof(el)
    proof = ["0x" + binascii.hexlify(p).decode() for p in proof]
    result = {
        "proof": proof,
        "value": str(value),
    }
    return result
