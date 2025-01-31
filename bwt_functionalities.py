'''
BURROWS-WHEELER TRANSFORMATION FUNCTIONALITIES
This script contains the functions that the network needs to manage the BW Transformations.
'''


# CALCULATE BWT FROM DNA SEQUENCE
# 1. add the terminator character ($)
# 2. create and sort the suffixes with the suffix array
# 3. extract the last column and return it as result
def bwt(input_sequence):
    input_sequence += "$"

    suffix_index_list = len(input_sequence)
    suffixes = [(input_sequence[i:], i) for i in range(suffix_index_list)]
    suffixes.sort(key = lambda x: x[0].upper())
    
    bwt_result = "".join(input_sequence[i - 1] for _, i in suffixes)
    return(bwt_result)    


# CALCULATE THE ORIGINAL DNA SEQUENCE FROM BWT
# 1. For each BWT character, create a list of tuples (character, index), then sort it
# 2. Create a list to take trace of positions and another to register the current one
# 3. Append the current character to the original DNA sequence string, then go to the next position
# 4. Return the final (original) DNA sequence
def inverse_bwt(bwt):
    if "$" not in bwt:
        raise ValueError("The BWT sequence must contain the '$' termination character.")

    bwt_sequence_length = len(bwt)

    indexed_bwt = [(character, index) for index, character in enumerate(bwt)]
    indexed_bwt.sort(key=lambda x: x[0].lower())
    
    first_column_index = [pair[1] for pair in indexed_bwt]
    current_position = bwt.index("$")
    
    original_dnasequence = [""] * bwt_sequence_length
    
    for i in range(bwt_sequence_length - 1, -1, -1): 
        original_dnasequence[i] = bwt[current_position]
        current_position = first_column_index[current_position]
    
    return "".join(original_dnasequence[::-1]).strip("$")


# APPLY THE FUNCTIONS
if __name__ == "__main__":
    starting_sequence = "ACGTGT"

    bwt_transformed_sequence = bwt(starting_sequence)
    print(bwt_transformed_sequence)
    
    inversed_sequence = inverse_bwt(bwt_transformed_sequence)
    print(inversed_sequence)