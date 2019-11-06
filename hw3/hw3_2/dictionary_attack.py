import time
from typing import List, Dict, Tuple
from functools import reduce
from hashlib import sha256
from itertools import product, chain
from tqdm import tqdm


def dictionary_attack(filenames: Tuple[str, str], couples: Dict[str, int], hashes: List[str]) -> Dict[str, str]:

    start_time = time.time()

    # Load the dictionaries
    words_list = map(lambda filename: read_lines(filename), filenames)
    words = reduce(chain, words_list)
    max_len = 10
    changed_words = ()

    cracked = {}
    i = 0
    # Apply common transformations to the dictionary
    print("Applying transformations")
    for word, encoding in tqdm(words, total=14344391):

        if len(word) > 15:
            continue

        for change in cartesian_changes(word, couples):
            i += 1
            sha = compute_sha(change)
            # print(change)
            if sha in hashes:
                cracked[sha] = change
                print("Found {psw} with hash {sha}".format(
                    psw=change, sha=sha))

            titled_change = change.title()
            if change != titled_change:
                # print(titled_change)
                i += 1
                sha_title = compute_sha(titled_change)
                if sha_title in hashes:
                    cracked[sha_title] = titled_change
                    print("Found {psw} with hash {sha}"
                          .format(psw=titled_change, sha=sha_title))

        if word.title() != word:
            # print(word.title())
            for change in cartesian_changes(word.title(), couples):
                i += 1
                sha = compute_sha(change)
                # print(change)
                if sha in hashes:
                    cracked[sha] = change
                    print("Found {psw} with hash {sha}".format(
                        psw=change, sha=sha))

    print("\nHashed {i} words\n".format(i=i))
    end_time = time.time()
    return cracked, end_time - start_time


def compute_sha(word: str, encoding='utf-8') -> str:
    h = sha256()
    h.update(word.encode(encoding))

    return h.hexdigest()


def read_lines(filename: str) -> List[str]:

    with open(filename[0], encoding=filename[1]) as f:
        while True:
            line = f.readline()
            if not line:
                break
            yield (line.strip(), filename[1])


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def cartesian_changes(word, couples):
    options = ((c,) if c not in couples else (
        c, str(couples[c])) for c in word)
    return (''.join(o) for o in product(*options))


def count_subst(word: str, couples: Dict[str, int]) -> int:
    return sum(map(lambda letter: word.count(letter), couples.keys()))
