import numpy as np
from bitstring import BitArray
from random import shuffle
from secrets import randbelow

MATRIX_SIZE = 3
SET_SIZE = 2004

"""
BITSTRING FUNCTIONS
"""

def random_bitarray():
    """
    Program generates a random number in the range (0, 2^SET_SIZE)
    and uses its binary representation to generate numbers in the set. 
    
    The xth entry of the BitArray corresponds to the number x being in
    the set.
    """
    
    numb = randbelow(2**SET_SIZE)
    return BitArray(uint = numb, length = SET_SIZE)


def permute_array(elem, perm):
    newBitStr = BitArray(uint = 0, length = SET_SIZE)
    for i in range(SET_SIZE):
        newBitStr.set(elem[perm[i]], i)
    
    return newBitStr



"""
PERMUTATION FUNCTIONS
"""

def permutation_product(permA, permB):
    """
    The two inputs are permutations (represented as lists in this
    program).
    """
    
    permC = np.empty(SET_SIZE, dtype=int)
    for i in range(SET_SIZE):
        permC[i] = permA[permB[i]]
    return permC



class MatrixWithSets():
    def __init__(self):
        self.matrix = []
        for i in range(MATRIX_SIZE):
            self.matrix.append([])
            for j in range(MATRIX_SIZE):
                self.matrix[i].append([])
        
        
    def __mul__(self, other):
        val = MatrixWithSets()
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                toInsert = (self.matrix[i][0] & other.matrix[0][j])
                for k in range(1, MATRIX_SIZE):
                    compareTo = self.matrix[i][k] & other.matrix[k][j]
                    toInsert |= compareTo
                    
                val.replace(i, j, toInsert)
        return val
    
    def __eq__(self, other):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True
    
    def __pow__(self, k):
        k_binary = bin(k)
        val = MatrixWithSets()
        val.identity()
        for digit in range(2, len(k_binary)):
            val *= val
            if (k_binary[digit] == "1"):
                val *= self
        
        return val

    def __str__(self):
        output = ""
        for i in range(MATRIX_SIZE):
                for j in range(MATRIX_SIZE):
                    text = "Entry ({0},{1}): ".format(i + 1, j + 1)
                    output += text + self.matrix[i][j].bin + "\n"
        return output
    
                
    def identity(self):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                if (i == j):
                    self.matrix[i][j] = BitArray(uint = 0, length = SET_SIZE)
                else:
                    self.matrix[i][j] = BitArray(uint = (2**SET_SIZE) - 1, length = SET_SIZE)
                    
    def randomize(self):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                self.matrix[i][j] = random_bitarray()
    
    def replace(self, row, col, b_str):
        self.matrix[row][col] = b_str
    

def permute_matrix(self, perm):
    newM = MatrixWithSets()
    for i in range(MATRIX_SIZE):
        for j in range(MATRIX_SIZE):
            newM.replace(i, j, permute_array(self.matrix[i][j], perm))
    return newM
    
def tuple_exponent(self, k):
    """
    This is the standard square-and-multiply algorithm
    applied to the tuples (M, h), M being a boolean matrix, h being
    a permutation
    """
    
    k_binary = bin(k)
    value = self
    for digit in range(3, len(k_binary)): 
        value = semidirect_product(value, value)[:]
        if (k_binary[digit] == "1"):
            value = semidirect_product(value, self)[:]
    
    return value  

def tuple_exponent_memoized(memo, k):
    """
    This is a modified version of square-and-multiply with
    memoization. Alleviates the cost of running multiple trials
    The input memo is the matrix containing (M, h) to powers of 2,
    and k is the power of the array.
    """
    k_binary = bin(k)
    value = memo[-1]
    for digit in range(3, len(k_binary)):
        if (k_binary[digit] == "1"):
            value = semidirect_product(value, memo[2 - (digit + 1)])[:]
    
    return value  

def semidirect_product(M_h, M_h_prime):
    """
    This is the standard semidirect product function
    The two inputs are two tuples of the form (M, h) and (M', h')
    """
    shuffled_matrix_M = permute_matrix(M_h[0], M_h_prime[1])
    first_elem = shuffled_matrix_M * M_h_prime[0]
    second_elem = permutation_product(M_h[1], M_h_prime[1])
    
    return (first_elem, second_elem)


def check_orbit(mh_tuple, k):
    stored_indices = []
    tuple_check = tuple_exponent(mh_tuple, k)
    key = mh_tuple
    for i in range(1, k):
        if (tuple_check[0] == key[0]):
            stored_indices.append(i)
        
        key = semidirect_product(key, (M, h))

    return stored_indices
    
    

# ----------------------------------------------------------------------
#                       PROTOCOL DESCRIPTION
# ----------------------------------------------------------------------

# STEP 1:
#   (i) Agree on a matrix M and permutation h
M = MatrixWithSets()
M.randomize()

h = np.arange(SET_SIZE)
np.random.shuffle(h)

#   (ii) Alice and Bob pick two random integers
a = randbelow(SET_SIZE)
b = randbelow(SET_SIZE)

print("Matrix M:")
print(M)
print("Permutation:\n", h)
print("a =", a)
print("b =", b)

# STEP 2:
AliceCalc = tuple_exponent((M, h), a)
print("\nFinished calculating A")

# STEP 3:
BobCalc = tuple_exponent((M, h), b)
print("Finished calculating B")

# STEP 4: Alice retrieves K_A
AliceKey = semidirect_product(BobCalc, AliceCalc)
K_A = AliceKey[0]

print("Finished calculating K_A")

# STEP 5: Bob retrieves K_B
BobKey = semidirect_product(AliceCalc, BobCalc)
K_B = BobKey[0]

print("Finished calculating K_B")

# STEP 6: Calculation of secret key K to confirm key generation works.
KeyCalculation = tuple_exponent((M, h), a + b)
K = KeyCalculation[0]

print("\nK_A")
print(K_A)
print("K_B")
print(K_B)
print("K")
print(K)

