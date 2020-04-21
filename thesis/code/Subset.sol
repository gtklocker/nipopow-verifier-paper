function subset(
    Proof memory exist, uint existLca,
    Proof memory cont, uint contLca
) internal pure returns(bool)
{
    uint256 j;
    for (uint256 i = 0; i < existLca; i++) {
        while (exist[i] != cont[j]) {
            if (++j >= contLca) { return false; }
        }
    }
    return true;
}
