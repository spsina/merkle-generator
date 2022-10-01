import json
from helpers import get_web3_object
from multicall import Multicall, Call
import csv

w3 = get_web3_object()


def load_csv_file(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data[1:]


def multi_fetch_maturity_time():
    nft_contract = "0x958C24d5cDF94fAF47cF4d66400Af598Dedc6e62"

    base_maturity_time = 1664571397
    whitelist = [441, 442]  # these addresses get the base maturity time

    sheet_data = load_csv_file("nft_sheet_new.csv")

    # nft_amount is the 3rd column in the sheet
    nft_amounts = {}
    for row in sheet_data:
        nft_amounts[row[1]] = int(float(row[2]) * 1e18)

    calls = []
    for row in sheet_data:
        nft_id = int(row[1])
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

    nft_data = []  #  {tokenId, amount, maturity_time}

    # the second argument is the maturity time
    for nft_id, info in result.items():
        maturity_time = info[1]
        if nft_id in whitelist:
            maturity_time = base_maturity_time
        nft_data.append(
            {
                "tokenId": nft_id,
                "amount": nft_amounts[str(nft_id)],
                "maturity_time": maturity_time,
            }
        )
    return nft_data


if __name__ == "__main__":
    result = multi_fetch_maturity_time()

    with open("nft_data.json", "w") as f:
        json.dump(result, f)
