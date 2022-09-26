import binascii
from flask import Flask
from flask_cors import CORS
from generate_nft_tree import generate_nft_tree

# dei_tree, dei_data = generate_dei_tree()
nft_tree, nft_data = generate_nft_tree()

app = Flask(__name__)
CORS(app)


@app.route("/nft/root/")
def get_nft_root():
    for _, node in nft_tree.tree.items():
        if node["parent"] is None:
            return {"root": binascii.hexlify(node["hash"]).decode()}


@app.route("/nft/proof/<token_id>/")
def get_nft_proof(token_id):
    token_id = int(token_id)
    token_data = nft_data[token_id]
    maturity_date = token_data["maturity_date"]
    amount = token_data["amount"]

    el = {
        "tokenId": token_id,
        "amount": amount,
        "maturity_date": maturity_date,
    }

    print(nft_tree.get_packed(el))
    proof = nft_tree.get_proof(el)
    proof = ["0x" + binascii.hexlify(p).decode() for p in proof]
    result = {
        "proof": proof,
        "value": token_data,
    }
    return result
