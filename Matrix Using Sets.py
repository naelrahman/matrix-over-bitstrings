import numpy as np
from bitstring import BitArray
from random import shuffle
from secrets import randbelow

MATRIX_SIZE = 3
SET_SIZE = 200

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
    k_binary = bin(k)
    value = self
    for digit in range(3, len(k_binary)): 
        value = semidirect_product(value, value)[:]
        if (k_binary[digit] == "1"):
            value = semidirect_product(value, self)[:]
    
    return value  


def semidirect_product(tupleA, tupleB):
    shuffleM = permute_matrix(tupleA[0], tupleB[1])
    firElem = shuffleM * tupleB[0]
    secElem = permutation_product(tupleA[1], tupleB[1])
    
    return (firElem, secElem)
    
    

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

