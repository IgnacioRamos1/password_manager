
import secrets
import hashlib


def seed_phrase():
    hex = (secrets.token_hex(16))

    binary = bin(int(hex, 16))[2:].zfill(128)

    numbers_binary = [binary[i:i+11] for i in range(0, len(binary), 11)]

    checksum = hashlib.sha256(numbers_binary[11].encode('utf-8')).hexdigest()
    checksum_binary = bin(int(checksum[0], 16))[2:].zfill(4)

    numbers_binary[11] = numbers_binary[11]+checksum_binary

    numbers_int = []

    for number in numbers_binary:
        number = int(number, 2)
        numbers_int.append(number)

    file = open("BIP39_Wordlist.txt", "r")
    content = file.readlines()

    seed = []

    for word in numbers_int:
        seed_word = content[word].strip('\n')
        seed.append(seed_word)

    print(seed)


seed_phrase()
