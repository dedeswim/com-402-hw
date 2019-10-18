import time
from typing import List, Dict, Tuple
from functools import reduce, partial
from hashlib import sha256
from itertools import combinations, chain
from tqdm import tqdm
from multiprocessing import Pool


def permute_letter_changes(psw: str, couples: List[Tuple[str, int]]) -> List[str]:
    lengths = range(len(couples) + 1)
    
    permuted_changes = list(map(
        lambda length: apply_n_letter_changes(psw, couples, length),
        lengths
    ))

    return [psw] + reduce(concat_lists, permuted_changes)

def apply_n_letter_changes(psw, couples, length):
    couples_combinations = combinations(couples, length)
    combinated_psw = list(map(
        lambda couples: apply_letter_changes(psw, couples),
        couples_combinations
    ))
    
    return combinated_psw

def apply_letter_changes(psw: str, couples: List[Tuple[str, int]]) -> List[str]:
    new_psw = psw
    for couple in couples:
        new_psw = new_psw.replace(couple[0], str(couple[1]))
    
    return new_psw

def create_dictionary(filenames: List[str], couples: Dict[str, int], threads=4) -> Dict[str, str]:
    
    start_time = time.time()
    transformations_filename = 'digitized_words.txt'
  
    # Load the dictionaries
    words_list = map(lambda filename: read_lines(filename), filenames)
    words = set(reduce(concat_lists, words_list))

    # Apply common transformations to the dictionary
    print("Applying transformations")
    transformer_partial = partial(recursive_letter_changes, couples=couples)
    
    with open(transformations_filename) as f:
        digitized_words = f.readlines()
        digitized_words = [word.strip() for word in digitized_words]

    if not digitized_words:
        with Pool(threads) as pool:
            changed_words_list = tqdm(pool.map(transformer_partial, words))
            digitized_words = set(reduce(concat_lists, changed_words_list))
    
    titled_word = set(list(digitized_words) + [word.title() for word in digitized_words])


    with open('digitized_words.txt', 'w') as f:
        for word in sorted(titled_word):
            f.write(word + '\n')

    print("Generating dictionary")
    dictionary = tqdm({compute_sha(psw): psw for psw in words})

    end_time = time.time()
    return dictionary, end_time - start_time

def recursive_letter_changes(psw: str, couples: Dict[str, int]) -> List[str]:
    if not psw:
        return ['']
    
    changed_list = []
    rest_list = recursive_letter_changes(psw[1:], couples)
    
    changed_list.append(list(map(lambda rest: psw[0] + rest, rest_list)))
    
    if psw[0] in couples:
        changed_list.append(list(map(lambda rest: str(couples[psw[0]]) + rest, rest_list)))
    
    return [val for sublist in changed_list for val in sublist]

def compute_sha(word: str) -> str:
    h = sha256()
    h.update(word.encode())
    
    return h.hexdigest()

def read_lines(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()

    return [line.strip() for line in lines]

def concat_lists(x: List, y: List) -> List:
    return x + y
