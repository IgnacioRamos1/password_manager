
import secrets
import hashlib


def divide_chunks(list, n):
    for i in range(0, len(list), n):
        yield list[i:i + n]


def seed_phrase():
    entropy_hex = (secrets.token_hex(16))

    entropy_binary = bin(int(entropy_hex, 16))[2:].zfill(128)

    n = 11
    numbers_binary = list(divide_chunks(entropy_binary, n))

    checksum = hashlib.sha256(numbers_binary[11].encode('utf-8')).hexdigest()
    checksum_binary = bin(int(checksum[0], 16))[2:].zfill(4)

    numbers_binary[11] = numbers_binary[11]+checksum_binary

    file = open("BIP39_Wordlist.txt", "r")
    content = file.readlines()

    seed = []

    for number in numbers_binary:
        seed_word = content[int(number, 2)].strip()
        seed.append(seed_word)

    seed_string = ' '.join(seed)

    return seed_string

