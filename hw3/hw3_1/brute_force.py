import time
from itertools import combinations, permutations
from hashlib import sha256
from tqdm import tqdm

def brute_force(lengths, chars, hashes):
    cracked = {}
    start_time = time.time()

    for length in lengths:
        chars_combinations = combinations(chars, length)

        for char_combination in tqdm(chars_combinations):
            char_permutations = permutations(char_combination)

            for char_permutation in char_permutations:
                permutation_string = ''.join(char_permutation)
                h = sha256()
                h.update(permutation_string.encode())
                h_result = h.hexdigest()

                if h_result in hashes:
                    cracked[h_result] = permutation_string
                    print(
                        "Found password {n}/{tot}!\n{h_result} : {char_combination} "
                            .format(
                                n=str(len(cracked)),
                                tot=str(len(hashes)),
                                h_result=h_result,
                                char_combination=permutation_string
                            )
                        )
                
                if len(cracked) == len(hashes):
                    end_time = time.time()
                    return cracked, start_time - end_time
