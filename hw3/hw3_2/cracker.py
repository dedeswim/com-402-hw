from hashlib import sha256
from dictionary_attack import dictionary_attack

hashes_filename = 'hashes.txt'
dictionary_filenames = [
    ('dictionaries/rockyou.txt', 'latin-1'),
]


with open(hashes_filename) as f:
    hashes = f.readlines()

hashes = [x.strip() for x in hashes]

couples = {
    'e': 3,
    'o': 0,
    'i': 1
}

cracked, total_time = dictionary_attack(dictionary_filenames, couples, hashes)

print(cracked)

print("\nTook in total {m} m {s} s."
        .format(m=str(total_time // 60), s=str(round(total_time % 60))))

with open('cracked.txt', 'w') as f:
    for key in cracked:
        f.write("{hash}: {password}\n".format(hash=key, password=cracked[key]))
    
    f.write("\nTook in total {m} m {s} s."
        .format(m=str(int(total_time // 60)), s=str(round(total_time % 60))))

