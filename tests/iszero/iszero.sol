pragma solidity ^0.6.0;


contract testComp {
    function compWithB0(uint256 input) public pure returns (bool) {
        bool f = false;
        for (uint256 i = 0; i < 1000; i++) {
            if (!(input & 1 == 0)) {
                f = true;
            }
        }
        return false;
    }

    function compWith1(uint256 input) public pure returns(bool){
        if (input%2 == 1) {
            return true;
        }
        return false;
    }
}
