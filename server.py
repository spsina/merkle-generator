import binascii
from flask import Flask
from flask_cors import CORS
from generate_dei_tree import generate_dei_tree
from generate_nft_tree import generate_nft_tree

# dei_tree, dei_data = generate_dei_tree()
nft_tree, nft_data = generate_nft_tree()

app = Flask(__name__)
CORS(app)


# @app.route("/dei/root/")
# def get_dei_root():
#     for _, node in dei_tree.dei_tree.items():
#         if node['parent'] is None:
#             return {
#                 'root': binascii.hexlify(node['hash']).decode()
#             }
#
#
# @app.route("/dei/proof/<address>/")
# def get_dei_proof(address):
#     value = dei_data[address]
#     el = {'address': address, 'value': value}
#     proof = dei_tree.get_proof(el)
#     proof = ["0x" + binascii.hexlify(p).decode() for p in proof]
#     result = {
#         'proof': proof,
#         'value': value,
#     }
#     return result


@app.route("/nft/root/")
def get_nft_root():
    for _, node in nft_tree.tree.items():
        if node['parent'] is None:
            return {
                'root': binascii.hexlify(node['hash']).decode()
            }


@app.route("/nft/proof/<token_id>/")
def get_nft_proof(token_id):
    token_id = int(token_id)
    value = nft_data[token_id]
    el = {'tokenId': token_id, 'amount': value}
    print(nft_tree.get_packed(el))
    proof = nft_tree.get_proof(el)
    proof = ["0x" + binascii.hexlify(p).decode() for p in proof]
    result = {
        'proof': proof,
        'value': value,
    }
    return result
