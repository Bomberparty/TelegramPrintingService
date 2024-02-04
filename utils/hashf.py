def my_hash(s):
    hash_value = 5381

    for c in s:
        hash_value = (hash_value * 33) ^ ord(c)

    hash_value &= 0xFFFFFFFF

    hash_value += hash_value == 0

    return hash_value
