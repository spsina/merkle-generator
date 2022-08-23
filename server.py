import binascii
from flask import Flask
from flask_cors import CORS
from generate_tree import generate_tree

tree, data = generate_tree()

app = Flask(__name__)
CORS(app)


@app.route("/root/")
def get_root():
    for _, node in tree.tree.items():
        if node['parent'] is None:
            return {
                'root': binascii.hexlify(node['hash']).decode()
            }


@app.route("/proof/<tokenIds>/")
def get_proof(tokenIds):
    result = {}
    for tokenId in tokenIds.spilit(','):
        amount = int(data[tokenId])
        proof = ["0x" + binascii.hexlify(p).decode() for p in tree.get_proof({'tokenId': tokenId, 'amount': amount})]
        result[tokenId] = {
            'proof': proof,
            'amount': amount,
        }
    return result
