import json
from helpers import get_web3_object
from multicall import Multicall, Call


w3 = get_web3_object()


def load_nft_ids():
    nft_ids = []
    with open("nft_ids.txt", "r") as f:
        for line in f:
            nft_ids.append(int(line.strip()))
    return nft_ids


def load_nft_amounts():
    file = open("nft_amount.json", "r")
    nft_amounts = json.load(file)
    return nft_amounts


def multi_fetch_maturity_time():
    nft_contract = "0x958C24d5cDF94fAF47cF4d66400Af598Dedc6e62"

    base_maturity_time = 1664571397
    whitelist = [441, 442]  # these addresses get the base maturity time

    nft_ids = load_nft_ids()

    calls = []
    for nft_id in nft_ids:
        calls.append(
            Call(
                w3,
                nft_contract,
                ["bondRedeems(uint256)(uint256,uint256)", nft_id],
                [[nft_id, None]],
            )
        )

    multicall = Multicall(w3, calls)
    result = multicall()

    nft_amount = load_nft_amounts()
    nft_data = []  #  {tokenId, amount, maturity_time}

    # the second argument is the maturity time
    for nft_id, info in result.items():
        maturity_time = info[1]
        if nft_id in whitelist:
            maturity_time = base_maturity_time
        nft_data.append(
            {
                "tokenId": nft_id,
                "amount": nft_amount[str(nft_id)],
                "maturity_time": maturity_time,
            }
        )
    return nft_data


if __name__ == "__main__":
    result = multi_fetch_maturity_time()

    with open("nft_data.json", "w") as f:
        json.dump(result, f)
