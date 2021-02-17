from bitstring import BitArray
from random import shuffle
from secrets import randbelow


MATRIX_SIZE = 3
SET_SIZE = 200



# Idea: Program generates a random number in the range (0, 2^100),
#   and uses it's binary representation to generate numbers in the set.
# Note: The first entry of the BitArray corresponds to 1 being in the set.
def RandomBitArray():
    numb = randbelow(2**SET_SIZE)
    return BitArray(uint = numb, length = SET_SIZE)
    

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
        # Starts at 2 to omit the "0b" part of binary representation.
        for digit in range(2, len(k_binary)):
            val *= val # Squares no matter what the binary digit is.
            if (k_binary[digit] == "1"): # Multiply by x when digit = 1.
                val *= self
        
        return val
    
    
    # Methods of turning matrix into a certain type   
    def randomize(self):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                self.matrix[i][j] = RandomBitArray()
                
    def identity(self):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                if (i == j): # Diagonals of matrix
                    self.matrix[i][j] = BitArray(uint = 0, length = SET_SIZE)
                else:
                    self.matrix[i][j] = BitArray(uint = (2**SET_SIZE) - 1, length = SET_SIZE)  
    
    
    
    def replace(self, row, col, b_str):
        self.matrix[row][col] = b_str
    
    def output(self):
        for i in range(MATRIX_SIZE):
                for j in range(MATRIX_SIZE):
                    text = "Entry ({0},{1}):".format(i + 1, j + 1)
                    print(text, self.matrix[i][j].bin)
    
    
    # Uses function ArrayOutput (currently unused)
    def output_list(self):
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                ArrayOutput(self.matrix[i][j])
            print()
    



def permute(bits, perm):
    


    
TO_SQUARE = 5000

print("\n")
print("ORIGINAL MATRIX A:", "\n")
a = MatrixWithSets()
a.randomize()
a.output()
print("\n", "---------------------------------------------------------------", "\n")

print("A MULTIPLIED", TO_SQUARE, "TIMES", "\n")
b = xk(a, TO_SQUARE)
b.output()

print("\n", "---------------------------------------------------------------", "\n")

u = BitArray(bin = '0011')
v = BitArray(bin = '0101')

x = u | v # Union (or)
y = u & v # Intersection (and)
z = u ^ v # (xor)
ArrayOutput(x)
ArrayOutput(y)
ArrayOutput(z)
