'''
BWT MANAGEMENT SERVER
This script contains the functions the server needs to manage requests
related to the Burrows-Wheeler Transformation of a DNA sequence.
'''

# IMPORT THE LIBRARIES NEEDED AND SET THE ENVIRONMENT FOR ERRORS
from flask import Flask, request, jsonify
import logging
import configparser
from bwt_functionalities import bwt, inverse_bwt

logging.basicConfig(level = logging.DEBUG)


# CREATE THE APIs FOR BOTHE THE BWT TRANSFORMATION AND ITS INVERSE
# 1. get the data
# 2. from the data, get the sequence to be transformed
# 3. transform the sequence and return it

application = Flask(__name__)

@application.route('/bwt', methods = ['POST'])
def endpoint_bwt():

    requested_data = request.get_json()
    application.logger.debug(f"The received data: {requested_data}")

    dna_sequence = requested_data.get('Sequence', '')
    application.logger.debug(f"The DNA sequence received to be BW-transformed: {dna_sequence}")

    # Try DNA -> BWT(DNA), if it doesn't work show an error :(
    try:
        bwt_result = bwt(dna_sequence)
        return jsonify(result = bwt_result)
    except ValueError as verr:
        application.logger.error(f"ERROR! Could not apply BWT to this sequence: {str(verr)}")
        return jsonify(error = str(verr)), 400


@application.route('/inverse_bwt', methods = ['POST'])
def endpoint_inverse_bwt():

    requested_data = request.get_json()
    application.logger.debug(f"The received data: {requested_data}")

    bwt_sequence = requested_data.get('BWT', '')
    application.logger.debug(f"The BWT sequence received to be transformed in DNA: {bwt_sequence}")

    # Try BWT(DNA) -> DNA, if it doesn't work show an error :(
    try:
        dna_result = inverse_bwt(bwt_sequence)
        return jsonify(result = dna_result)
    except ValueError as verr:
        application.logger.error(f"ERROR! Could not reverse this BWT sequence: {str(verr)}")
        return jsonify(error = str(verr)), 400
    

# NETWORK MANAGEMENT
if __name__ == '__main__':

    # Configure host and port from configurator.cfg file
    configurator = configparser.ConfigParser()
    configurator.read('configurator.cfg')
    host = configurator.get(section = 'Server', option = 'host')
    port = configurator.getint(section = 'Server', option = 'port')

    # Run the application with the configured values
    application.run(host = host, port = port)