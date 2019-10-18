from hashlib import sha256
from dictionary_attack import dictionary_attack

hashes_filename = 'hashes.txt'
dictionary_filenames = [
    # 'dictionaries/john.txt',
    # 'dictionaries/500-worst-passwords.txt',
    # 'dictionaries/cain.txt',
    # 'dictionaries/conficker.txt',
    # 'dictionaries/twitter-banned.txt',
    # 'dictionaries/english.txt',
    # 'dictionaries/probable-v2-top12000.txt',
    ('dictionaries/rockyou.txt', 'latin-1'),
    # ('dictionaries/realhuman_phill.txt', 'latin-1')
]


with open(hashes_filename) as f:
    hashes_salts = f.readlines()

hashes_salts = [x.strip().split(',') for x in hashes_salts]
hashes = [x[0] for x in hashes_salts]
salts = [x[1] for x in hashes_salts]

couples = {
    'e': 3,
    'o': 0,
    'i': 1
}

cracked, total_time = dictionary_attack(dictionary_filenames, couples, hashes, salts)

print(cracked)

print("\nTook in total {m} m {s} s."
        .format(m=str(total_time // 60), s=str(round(total_time % 60))))

with open('cracked.txt', 'w') as f:
    for key in cracked:
        f.write("{hash}: {password}\n".format(hash=key, password=cracked[key]))
    
    f.write("\nTook in total {m} m {s} s."
        .format(m=str(int(total_time // 60)), s=str(round(total_time % 60))))

