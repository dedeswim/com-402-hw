from brute_force import brute_force
from threaded_brute_force import multi_thread_brute_force

filename = 'hashes.txt'
lengths = [4, 5, 6]
chars = list("abcdefghijklmnopqrstuvwxyz0123456789")

with open(filename) as f:
    hashes = f.readlines()

hashes = [x.strip() for x in hashes]

cracked, total_time = multi_thread_brute_force(lengths, chars, hashes)

print(cracked)
print("\nTook in total {m} m {s} s."
        .format(m=str(total_time // 60), s=str(round(total_time % 60))))

with open('cracked.txt', 'w') as f:
    for key in cracked:
        f.write("{hash}: {password}\n".format(hash=key, password=cracked[key]))
    
    f.write("\nTook in total {m} m {s} s."
        .format(m=str(int(total_time // 60)), s=str(round(total_time % 60))))