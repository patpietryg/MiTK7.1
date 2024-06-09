import random

cipher_key = {
    'A': ['@', '1'],
    'B': ['#', '2'],
    'C': ['$', '3'],
    'D': ['%', '4'],
    'E': ['&', '5'],
    'F': ['*', '6'],
    'G': ['+', '7'],
    'H': ['-', '8'],
    'I': ['!', '9'],
    'J': ['?', '0'],
    'K': ['~', 'a'],
    'L': ['^', 'b'],
    'M': ['_', 'c'],
    'N': ['=', 'd'],
    'O': ['{', 'e'],
    'P': ['}', 'f'],
    'Q': ['[', 'g'],
    'R': [']', 'h'],
    'S': ['|', 'i'],
    'T': ['\\', 'j'],
    'U': [':', 'k'],
    'V': [';', 'l'],
    'W': ['"', 'm'],
    'X': ["'", 'n'],
    'Y': ['<', 'o'],
    'Z': ['>', 'p']
}

def encrypt_homophonic(text, key):
    encrypted_text = ''
    for char in text.upper():
        if char in key:
            encrypted_text += random.choice(key[char])
        else:
            encrypted_text += char
    return encrypted_text

def decrypt_homophonic(encrypted_text, key):
    reverse_key = {}
    for letter, symbols in key.items():
        for symbol in symbols:
            reverse_key[symbol] = letter

    decrypted_text = ''
    for char in encrypted_text:
        if char in reverse_key:
            decrypted_text += reverse_key[char]
        else:
            decrypted_text += char
    return decrypted_text


def encrypt_columnar_transposition(text, key):
    text = text.replace(" ", "")

    n = len(key)
    while len(text) % n != 0:
        text += "X"

    grid = [''] * n
    for i in range(len(text)):
        grid[i % n] += text[i]

    key_indices = sorted(range(len(key)), key=lambda k: key[k])
    encrypted_text = ''.join([grid[i] for i in key_indices])

    return encrypted_text


def decrypt_columnar_transposition(encrypted_text, key):
    n = len(key)
    m = len(encrypted_text)
    num_rows = m // n

    grid = [''] * n
    start = 0
    for i in range(n):
        grid[i] = encrypted_text[start:start + num_rows]
        start += num_rows

    key_indices = sorted(range(len(key)), key=lambda k: key[k])
    ordered_grid = [''] * n
    for i, idx in enumerate(key_indices):
        ordered_grid[idx] = grid[i]

    decrypted_text = ''
    for i in range(num_rows):
        for j in range(n):
            decrypted_text += ordered_grid[j][i]

    decrypted_text = decrypted_text.rstrip('X')

    return decrypted_text
def encrypt_combined(text, homo_key, trans_key):
    encrypted_text = encrypt_homophonic(text, homo_key)
    final_encrypted_text = encrypt_columnar_transposition(encrypted_text, trans_key)
    return final_encrypted_text

def decrypt_combined(encrypted_text, homo_key, trans_key):
    decrypted_text = decrypt_columnar_transposition(encrypted_text, trans_key)
    final_decrypted_text = decrypt_homophonic(decrypted_text, homo_key)
    return final_decrypted_text


with open('text.txt', 'r') as file:
    plain_text = file.read()

column_key = "3142"

encrypted_text = encrypt_combined(plain_text, cipher_key, column_key)
decrypted_text = decrypt_combined(encrypted_text, cipher_key, column_key)

with open('encrypted_text.txt', 'w') as file:
    file.write(encrypted_text)

with open('decrypted_text.txt', 'w') as file:
    file.write(decrypted_text)

print(f"Tekst jawny: {plain_text}")
print(f"Tekst zaszyfrowany zapisany w encrypted_text.txt")
print(f"Tekst odszyfrowany zapisany w decrypted_text.txt")
