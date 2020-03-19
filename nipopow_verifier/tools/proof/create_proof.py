"""
This file contains useful functions to export and import proofs.
The proofs are stored to and imported from .pkl files.
The names of the proofs are refering to the chain they were created by.
For example, proof_100.pkl contains a proof created by a 100-sized Blockchain.
Notice that the size of the proof is different.

The iteration of the proofs behins from the last block.

 Genesis
 |
 |
 v    proof
 --------------->
 ^              ^
 |              |
 block[-1]      block[0]

------------------------------------------------------------------------------------------

It is possible to generate fork proofs. That is, proofs of a chain that has a
common ancestor with another one.


 Block of interest contained in both chains
 --------+-------->  Pa
         |
         +--->       Pb

The name of the fok chain is proof_<B>_-<>_<b>

Where
B: Size:        The nuumber of blocks of the original chain
: Fork index:  The index of the common ancestor of the two chains
b: Fork blocks: The number of block included only to the forked chain

"""

import sys
import argparse
import pickle
import create_blockchain_new as blockchain_utils


class ProofTool:
    """
    pt = ProofTool("proof.pkl")
    pt.fetch_proof()
    """

    def __init__(self, proofs_dir="../data/proofs/"):
        self.dir = proofs_dir

    def proof_dir(self):
        """
        Returns the path of the proof folder
        """
        return self.dir

    def make_proof_filename(self, blocks):
        """
        Returns the name of the proof name with regard to the size of the underlying chain
        """
        return self.proof_dir() + "proof_" + str(blocks) + ".pkl"

    def import_proof(self, blocks=None, filename=None):
        """
        Loads a proof from a .pkl file. The file must exist.
        """
        if blocks is None and filename is None:
            raise NameError(
                "You need to provide number of blocks or filename for proof"
            )
        if filename is None:
            filename = self.make_proof_filename(blocks)
        pickle_in = open(filename, "rb")
        proof = pickle.load(pickle_in)
        print("Proof loaded from " + filename)
        return proof

    @staticmethod
    def export_proof(proof, filename):
        """
        Stores a proof to a .pkl file. If exists, the file is overridden
        """
        pickle_out = open(filename, "wb")
        pickle.dump(proof, pickle_out)
        pickle_out.close()
        print("Proof was written in " + filename)

    def create_proof(self, blocks, filename=None):
        """
        Creates a chain with the given block number, constracts the
        corresponding proof and stores the proof in a .pkl file
        """
        header, header_map, interlink_map = blockchain_utils.create_blockchain(
            blocks=blocks
        )
        proof = blockchain_utils.make_proof(header, header_map, interlink_map)
        if filename is None:
            filename = self.make_proof_filename(blocks)
        self.export_proof(proof, filename)
        return proof

    def make_fork_proof_filename(self, mainblocks, fork_index, forkblocks):
        """
        Returns the name of the proof name with regard to the size of the
        underlying main chain and fork chain

        Genesis
        |
        v
        --------+----------->   Main proof (size 100)
                |
        ^       +----->     ^   Fork proof (size  70)
        |                   |
        |       ^     ^     |
        |       |     |     |
        100    50    20     0   Main fork index

        <---size 70--->
        <------size 100----->

        main proof: proof_100.pkl
        fork chain: proof_100_-50_+20.pkl

        For the above example, this would return:
        proof_100_-50_+20.pkl
        """
        return (
            self.proof_dir()
            + "proof_"
            + str(mainblocks)
            + "_-"
            + str(fork_index)
            + "_+"
            + str(forkblocks)
            + ".pkl"
        )

    def fetch_proof_by_blocks(self, blocks):
        """
        Returns a proof generated by a chain of the size of the given number
        of blocks If the proof doesn't exist, it will be created according to
        the name convension If the proof exists, it will be imported from the
        proof directory
        """

        try:
            proof = self.import_proof(blocks)
        except IOError:
            filename = self.make_proof_filename(blocks)
            print("File", filename, "does not exist. Creating...")
            proof = self.create_proof(blocks)
        except NameError as err:
            raise err
        finally:
            print("...ok")

        return proof

    def fetch_proof_by_name(self, filename):
        """
        Returns a proof with the provided name
        """

        return self.import_proof(blocks=None, filename=filename)

    def fetch_proof(self, arg):
        """
        if arg is an int, returns a proof which was created by this amount of
        blocks
        if arg is string, returns a proof with that name
        """

        proof = []
        if isinstance(arg, str):
            proof = self.fetch_proof_by_name(arg)
        elif isinstance(arg, int):
            proof = self.fetch_proof_by_blocks(arg)
        else:
            raise ValueError("Argument must be either int or str")

        return proof

    def create_fixed_fork_proof(self, proof, fork_proof):
        """
        Creates the subset of the fork_proof which different than the original
        """

        lca = 0
        fixed_fork_proof = []

        for fp in fork_proof:
            try:
                lca = proof.index(fp)
                break
            except ValueError as e:
                fixed_fork_proof.append(fp)
                continue

        return fixed_fork_proof, lca - 1

    def create_proof_and_forkproof(self, mainblocks, fork_index, forkblocks):
        """
        Returns the names of a mainchain proof and a forkchain proof.
        If either of the two proofs does not exist, it is created with the known name convension
        See documentation of 'make_fork_proof_filename()'
        """

        # Initial blockchain
        header = None
        header_map = None
        interlink_map = None
        blockchain_name = self.proof_dir() + "blockchain_" + str(mainblocks) + ".pkl"
        try:
            open(blockchain_name)
            header, header_map, interlink_map = blockchain_utils.load_blockchain(
                blockchain_name
            )
        except Exception:
            (header, header_map, interlink_map) = blockchain_utils.create_blockchain(
                blocks=mainblocks
            )
            blockchain_utils.save_blockchain(
                blockchain_name, header, header_map, interlink_map
            )
        # Initial proof
        proof = []
        proof_name = self.make_proof_filename(mainblocks)
        proof = blockchain_utils.make_proof(header, header_map, interlink_map)

        # Fork blockchain
        fork_header = None
        fork_header_map = None
        fork_interlink_map = None
        f_header = header
        fork_blockchain_name = (
            self.proof_dir()
            + "blockchain_"
            + str(mainblocks)
            + "-"
            + str(fork_index)
            + "+"
            + str(forkblocks)
            + ".pkl"
        )

        # TODO: Chech if the fork blockchain can be exported as well
        (
            fork_header,
            fork_header_map,
            fork_interlink_map,
        ) = blockchain_utils.create_fork(
            f_header,
            header_map.copy(),
            interlink_map.copy(),
            fork=fork_index,
            blocks=forkblocks,
        )
        blockchain_utils.save_blockchain(
            fork_blockchain_name, fork_header, fork_header_map, fork_interlink_map
        )
        # Fork proof
        fork_proof = []
        fork_proof_name = self.make_fork_proof_filename(
            mainblocks, fork_index, forkblocks
        )
        fork_proof = blockchain_utils.make_proof(
            fork_header, fork_header_map, fork_interlink_map
        )

        fixed_fork_proof, lca = self.create_fixed_fork_proof(proof, fork_proof)
        self.export_proof(fixed_fork_proof, fork_proof_name)

        return (proof_name, fork_proof_name, lca)


def main():
    """
    Test for creating proofs
    """

    parser = argparse.ArgumentParser(
        description="Create and store proof from create_blockchain_new.py"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--blocks", type=int, help="Number of blocks")
    group.add_argument("--proof", type=str, help="Name of proof")
    args = parser.parse_args()
    blocks = args.blocks
    proof_name = args.proof

    proof_tool = ProofTool("../../data/proofs/")

    proof = []
    if blocks is not None:
        # proof = proof_tool.fetch_proof(blocks)
        proof = proof_tool.create_proof(blocks)
    elif proof_name is not None:
        proof = proof_tool.fetch_proof(proof_name)
    else:
        print("Provide --blocks or --proof argument")
        sys.exit()

    print("Proof size:", len(proof))


if __name__ == "__main__":
    main()
