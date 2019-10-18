from itertools import combinations_with_replacement, permutations, repeat
from hashlib import sha256
import time
from multiprocessing.dummy import Pool as ThreadPool, Value
from functools import reduce
from collections import ChainMap
from tqdm import tqdm

def combination_bf(char_combination, hashes_dict, found):
    cracked = {}

    char_permutations = set(permutations(char_combination))

    for char_permutation in char_permutations:
        permutation_string = ''.join(char_permutation)
        h = sha256()
        h.update(permutation_string.encode())
        h_result = h.hexdigest()

        if h_result in hashes_dict:
            cracked[h_result] = permutation_string
            found.value += 1
            print(
                "Found password {n}/{tot}!\n{h_result} : {char_combination} "
                    .format(
                        n=str(found.value),
                        tot=str(len(hashes_dict)),
                        h_result=h_result,
                        char_combination=permutation_string
                    )
                )
            
            if found.value == len(hashes_dict):
                return cracked

    return cracked

def multi_thread_brute_force(lengths, chars, hashes, threads=4):
    start_time = time.time()
    found = Value('i', 0)
    hashes_dict = {key: '' for key in hashes}

    total = sum(map(lambda x: len(chars) ** 6, lengths))
    print("Total combinations to be checked: " + str(total))

    total_cracked = []

    for length in lengths:
        chars_combinations = combinations_with_replacement(chars, length)
        with ThreadPool(threads) as pool:
            cracked_iter = list(tqdm(pool.imap(
                lambda comb: combination_bf(comb, hashes_dict, found), chars_combinations, chunksize=100
            )))
        
        cracked = dict(ChainMap(*cracked_iter))
        total_cracked.append(cracked)

    total_cracked_dict = dict(ChainMap(*total_cracked))

    end_time = time.time()
    return total_cracked_dict, end_time - start_time
