"""
Contains information in the context of nipopow verifier
"""

import json

genesis = b"\xf3\x0cF\xbe\xc5B\xa3t9\x95.\x0f\xfe\x0ea\r\xbb\xcd\xad\x97\xee\xd9\xba\x94U\xdc\x90\x05\xcbW\xfcR"
m = 6
k = 6

profiler = "/home/stelios/Projects/solidity-gas-profiler/profile.js"

errors = {
    "merkle": "Merkle verification failed",
    "stack": "Stack length <= 0",
    "branch": "Branch length too big",
    "merkle_index": "Merkle index too big",
    "ante up": "insufficient collateral",
    "boi not exist": "Block of interest index is out of range",
    "period expired": "The submission period has expired",
    "proof exists": "A proof with this evens exists",
    "genesis": "Proof does not include the genesis block",
    "expire": "Contesting period has expired",
    "lca": "Lca out of range",
    "boi in sub-chain": "Block of interest exists in sub-chain",
    "existing proof": "Wrong existing proof",
    "wrong lca": "Wrong lca",
    "same proofs": "Contesting proof[1:] is not different from existing[lca+1:]",
    "low score": "Existing proof has greater score",
    "valid existing": "Existing proof is valid at this index",
}


def extract_message_from_error(err):
    """
    Returns the error message of the exception generated by failed require
    """

    data = json.loads(str(err.value).replace("'", '"'))["data"]
    data_l = list(data.keys())
    return data[data_l[0]]["reason"]
