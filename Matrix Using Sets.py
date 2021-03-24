from math import floor
from math import sqrt
from permutation import Permutation
from bitstring import BitArray
from random import shuffle
from random import randint
from secrets import randbelow

MATRIX_SIZE = 3
SET_SIZE = 200
POWER_BITS = 200

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
    return list(perm.permute(elem))



"""
PERMUTATION FUNCTIONS
"""

def generate_permutation(size):
    """
    Input should be SET_SIZE
    Special cases are 2 and 3, where a random shuffling of integers
    are used as the permutation.
    Else loop works as follows:
        - Finds primes uses Sieve of Eratosthenes until sum of generated
          primes (subcycle_length) exceeds size.
        - Removes last number if subcycle_length is bigger than size.
        - Uses subcycle_length to pull permutations out of the shuffled
          list of integers.
    """
    
    shuffled_nums = [(i + 1) for i in range(size)]
    shuffle(shuffled_nums)
    
    if (size == 2 or size == 3):
        return Permutation.cycle(*shuffled_nums)
    else:
        bool_vals = [True for i in range(2, size)]
        subcycle_lengths = []
        
        j = 0
        while(sum(subcycle_lengths) < size and j < size - 2):
            if (bool_vals[j] == True):
                cur_val = 2
                while ((j + 2) * cur_val < size):
                    bool_vals[((j + 2) * cur_val) - 2] = False
                    cur_val += 1
                subcycle_lengths.append(j + 2)
            j += 1
        
        if (sum(subcycle_lengths) > size):
            subcycle_lengths.pop()
        
        perm = Permutation.cycle()
        start = 0
        for num in subcycle_lengths:
            perm *= Permutation.cycle(*shuffled_nums[start:start + num])
            start += num
            
        return perm


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
                    self.matrix[i][j] = BitArray(uint = 0,
                        length = SET_SIZE)
                else:
                    self.matrix[i][j] = BitArray(uint = (2**SET_SIZE)-1,
                        length = SET_SIZE)
                    
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
    second_elem = M_h[1] * M_h_prime[1]
    
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

h = generate_permutation(SET_SIZE)

#   (ii) Alice and Bob pick two random integers of POWER_BITS bits
a = randint(2**(POWER_BITS-1), 2**POWER_BITS)
b = randint(2**(POWER_BITS-1), 2**POWER_BITS)

print("Matrix M:")
print(M)
print("Permutation:", h)
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

if (K_A == K_B):
    print("Alice and Bob's Keys are the same...")
    
if (K == K_A):
    print("Alice's Key is equal to the actual key.")


