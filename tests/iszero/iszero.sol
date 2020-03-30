pragma solidity ^0.6.0;

contract test {
    function func(uint256 input) public pure returns(bool){
        // if (input%2 == 1) {
        if (!(input%2 == 0)) {
            return true;
        }
        return false;
    }
}
