from flask import Flask

from generate_tree import generate_tree

tree, data = generate_tree()

app = Flask(__name__)


@app.route("/root/")
def get_root():
    for _, node in tree.tree.items():
        if node['parent'] is None:
            return {
                'root': node['hash']
            }


@app.route("/proof/<tokenId>/")
def get_proof(tokenId):
    amount = int(data[tokenId])
    proof =  tree.get_proof({'tokenId': tokenId, 'amount': amount})
    return {
        'proof': proof,
        'amount': amount,
    }
