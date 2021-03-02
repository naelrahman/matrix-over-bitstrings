import pickle
import bitstring
from matplotlib.backends.backend_pdf import PdfPages

MATRIX_SIZE = 3
SET_SIZE = 200
POWER_BITS = 2000
NUM_TRIALS = 1000

with open('1000_trials.pickle', 'rb') as f:
    data = pickle.load(f)

"""
    This is how the data is structured:
    (M.self_data(), h, A_SAVE, B_SAVE, KA_SAVE, KB_SAVE)
    
    Example: data[4][52][1][2].bin[138] is the 138th entry of (2, 3) of K_A of the 52nd
    trial.
"""

tableOne = [0, 0, 0] # Entries 17, 89, 128 of (1, 1)
tableTwo = [0, 0, 0] # Entries 1, 57, 183 of (2, 3)

for x in range(NUM_TRIALS):
    if data[5][x][0][0].bin[17] == '1':
        tableOne[0] += 1
    if data[4][x][0][0].bin[89] == '1':
        tableOne[1] += 1
    if data[4][x][0][0].bin[128] == '1':
        tableOne[2] += 1

    if data[4][x][1][2].bin[1] == '1':
        tableTwo[0] += 1
    if data[4][x][1][2].bin[57] == '1':
        tableTwo[1] += 1
    if data[4][x][1][2].bin[183] == '1':
        tableTwo[2] += 1
        
print(tableOne)
print(tableTwo)

totalZeroes = 0
totalOnes = 0
for x in range(NUM_TRIALS):
    for y in range(SET_SIZE):
        if data[5][x][0][1].bin[y] == '1':
            totalOnes += 1
        if data[5][x][0][1].bin[y] == '0':
            totalZeroes += 1
            
print(totalOnes)
print(totalZeroes)
    
