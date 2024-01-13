def my_hash(s):
    # Initialize hash value to a prime number
    hash_value = 5381

    # Loop through each character in the string
    for c in s:
        # Multiply hash value by a prime number
        hash_value = (hash_value * 33) ^ ord(c)

    # Mask the hash value to 32 bits to avoid collisions
    hash_value &= 0xFFFFFFFF

    # Ensure first 2^32 values are unique
    hash_value += hash_value == 0

    return hash_value
