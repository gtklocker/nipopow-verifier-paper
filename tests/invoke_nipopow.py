"""
Run with
python test_backends.py --blocks=10 --backend=Py-EVM
"""

import sys

sys.path.append("../tools/proof/")
from proof import Proof
from create_proof import ProofTool

from contract_api import (
    make_interface,
    submit_event_proof,
    submit_contesting_proof,
)
from config import extract_message_from_error, genesis

import argparse

import pickle


def main():
    """
    Test for backends
    """

    pt = ProofTool("../data/proofs/")
    proof = Proof()
    proof.set(pt.fetch_proof(500))

    # interface = make_interface("geth")
    # address = interface.get_contract().address
    # abi = interface.get_contract().abi
    # contract_file = open("contract",'wb')
    # pickle.dump({"address": address, "abi": abi}, contract_file)
    # contract_file.close()

    contract_file = open("contract", "rb")
    contract = pickle.load(contract_file)
    address = contract["address"]
    abi = contract["abi"]

    interface = make_interface("geth", {"address": address, "abi": abi})

    res = submit_event_proof(interface, proof, 10)
    # print(res["events"])
    # headers = res["events"]["headers"]
    # siblings = res["events"]["siblings"]
    # print(headers == proof.headers)
    # print(siblings == proof.siblings)
    # print(res["gas"])

    interface.end()


main()
