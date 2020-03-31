pragma solidity ^0.6.0;

contract testComp {
    function compWith0(uint256 input) public pure returns(bool){
        if (!(input%2 == 0)) {
            return true;
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
