'''
BWT MANAGEMENT CLIENT
This script contains the functions the client needs to send requests
related to the Burrows-Wheeler Transformation of a DNA sequence.
'''

# IMPORT THE LIBRARIES NEEDED
import requests
import argparse
#from fasta_functionalities import read_fasta


# TO TAKE THE DNA SEQUENCE FROM AN INPUT FASTA FILE
# 1. read the FASTA file
# 2. extract every line besides the header
def read_fasta(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    sequence = ""
    for line in lines:
        if not line.startswith(">"):
            sequence += line.strip()
    return sequence

# TO SUBMIT A REQUEST TO THE SERVER
# 1. Build the url
# 2. Send the request
# 3. Get the answer / show error message
def request_to_server(data, endpoint, host, port):
    url = f"http://{host}:{port}/{endpoint}"
    print(f"Submitting the data ({data}) in your request to this URL: {url}.")

    try:
        answer = requests.post(url, json = data)
        answer.raise_for_status()

        print(f"The status code of the answer is {answer.status_code}")
        print(f"The answer text is {answer.text}")

        return answer.json()

    except requests.exceptions.RequestException as rexc:
        print(f"ERROR! {rexc}")
        return None # in case of error, avoid the program to stop
    

# EXECUTE THE PROGRAM
# 1. Define the parameters that the user can specify from the command line
# 2. Depending on the input format, prepare different data to send
# 3. Send the request to the server and visualize the answer
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'Client in the BWT Network')
    parser.add_argument('--host', help = "Server host", required = True)
    parser.add_argument('--port', help = "Server port", required = True)
    parser.add_argument('--dnasequence', help = "DNA sequence")
    parser.add_argument('--bwt', help = "BWT(DNA) sequence")
    parser.add_argument('--fasta', help = "Path to the FASTA file")
    arguments = parser.parse_args()

    if arguments.fasta: # FASTA file format
        dna_sequence = read_fasta(arguments.fasta)
        endpoint = "bwt"
        data = {"Sequence": dna_sequence}
    elif arguments.dnasequence: # DNA sequence
        endpoint = "bwt"
        data = {"Sequence": arguments.dnasequence}
    elif arguments.bwt: # BWT sequence
        endpoint = "inverse_bwt"
        data = {"BWT": arguments.bwt}
    else:
        raise ValueError("You must provide at least one among a --fasta file, or a --dnasequence, or a --bwt input!")

    print(f"The arguments provided are: {arguments}")

    answer = request_to_server(data, endpoint, arguments.host, arguments.port)

    print(f"The final answer is: {answer}")