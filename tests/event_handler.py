from web3.auto import w3
import asyncio
import pickle

import sys

sys.path.append("../tools/proof/")
import create_blockchain_new as cb


def handle_event(event):
    log = dict(event)["args"]
    headers = log["headers"]
    siblings = log["siblings"]
    print(len(headers))
    print(len(siblings))
    # if cb.verify_proof():
    #     print("Proof was OK!")


async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)


def main():

    print("Lintening...")

    contract_file = open("contract", "rb")
    contract = pickle.load(contract_file)

    address = contract["address"]
    abi = contract["abi"]

    contract = w3.eth.contract(address=address, abi=abi)

    event_filter = contract.events.debug.createFilter(fromBlock="latest")
    block_filter = w3.eth.filter("latest")
    tx_filter = w3.eth.filter("pending")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                # log_loop(tx_filter, 2),
                log_loop(event_filter, 2)
            )
        )
    finally:
        loop.close()


if __name__ == "__main__":
    main()
