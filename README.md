# set-key-exchange
Tagline: Implementation for a key exchange using matrices with entries as sets of numbers

This is a project I am working on with Prof. Vladimir Shpilrain of City College.
A link to his research can be found here: http://shpilrain.ccny.cuny.edu/res.html



About the implementation:

To implement the matrices, a custom class was created with entries as bitstrings. For the ith entry of a matrix, if the jth value is 0, then the number j+1 is not in the set. Similarly, if the jth entry is 1, the number j+1 is in the set. The dimensions of the matrix, and the size of the sets (aka the number of entries in the bitstring) can be set in the function by adjusting MATRIX_SIZE and SET_SIZE respectively.

Matrix multiplication consists of the following: entries being multiplied corresponds to the OR operator, and entries being added corresponds to the AND operator. An example of this is described in the pre-print (currently not up yet).

The key exchange uses the semi-direct product of these matrices, which is possible because of the ring structure of the set. The tuple multiplication can be found under semidirect_product.


Thanks for checking out this project!
                        
