import json
from Crypto.Hash import keccak


class MerkleTree:
    def __init__(self, data=[]) -> None:
        self.data = data
        self.tree = {}
        self.root = None

    def load_from_file(self, path):
        self.tree = json.loads(open(path).read())
        self.update_root()
        return self

    def get_proof(self, el):
        proof = []

        el_hash = self.get_hash(json.dumps(el))

        if el_hash not in self.tree.keys():
            return proof

        node = self.tree[el_hash]

        while node["parent"]:
            proof.append(node["sister"])
            node = self.tree[node["parent"]]

        return proof

    def update_root(self):
        for _, node in self.tree.items():
            if node["parent"] is None:
                self.root = node["hash"]

    def get_hash(self, el):
        k = keccak.new(digest_bits=256)
        k.update(el.encode())
        return str(k.hexdigest())

    def get_parent_hash(self, l, r):
        return self.get_hash("".join(list(sorted([l, r]))))

    def verify(self, el, proof):
        el_hash = self.get_hash(json.dumps(el))
        _hash = el_hash

        for _proof in proof:
            _hash = self.get_parent_hash(_hash, _proof)

        return self.tree[_hash]["parent"] is None

    def generate_tree(self):
        for el in self.data:
            el_hash = self.get_hash(json.dumps(el))
            self.tree[el_hash] = {
                "hash": el_hash,
                "content": el,
                "parent": None,
                "sister": None,
            }
        keys = list(self.tree.keys())

        while len(keys) > 1:
            tmp_keys = []
            for i in range(0, len(keys), 2):
                l = self.tree[keys[i]]

                if i + 1 < len(keys):
                    r = self.tree[keys[i + 1]]
                else:
                    r = self.tree[keys[i]]

                lr_hash = self.get_parent_hash(l["hash"], r["hash"])
                self.tree[lr_hash] = {
                    "hash": lr_hash,
                    "parent": None,
                    "content": None,
                    "sister": None,
                }

                l["parent"] = r["parent"] = lr_hash
                l["sister"], r["sister"] = r["hash"], l["hash"]
                tmp_keys.append(lr_hash)
            keys = tmp_keys

        self.update_root()
